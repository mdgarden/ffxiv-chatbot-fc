import os
from random import randint
import sys

from flask import Flask, request, abort, json
from pymongo import MongoClient

from dotenv import load_dotenv
from src import command, search
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    SourceGroup,
    SourceRoom,
)

from src.ingame import get_eorzea_time

# take environment variables from .env
load_dotenv()
app = Flask(__name__)


def get_group_list():
    with MongoClient(os.getenv("MONGO_URL")):
        db = MongoClient(os.getenv("MONGO_URL")).tweetify
        group_list = list(db.users.find())
    return group_list


group_list = get_group_list()
YOSHIDA = ["요시다아아아아", "요시다!!!!!", "요시다?", "요시다...."]


# get channel_secret and channel_access_token from your environment variable
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
channel_secret = os.getenv("LINE_CHANNEL_SECRET")

if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/")
def hello_world():
    return "Application is Running!"


@app.route("/tweet", methods=["POST"])
def new_tweet():
    # get request body as text
    body = request.get_data(as_text=True)

    response = app.response_class(
        response=json.dumps(body), status=200, mimetype="application/json"
    )
    data = json.loads(body)

    # format message
    text = data["text"]
    link = data["link"]
    message = text + "\n\n\n" + link
    print(message)
    group_list = get_group_list()
    try:
        for group in group_list:
            print("group")
            print(group)
            if (
                group["status"] == os.getenv("STATUS")
                and group["region"] == data["region"]
            ):
                line_bot_api.push_message(
                    group["room_id"], [TextSendMessage(text=message)]
                )
                print("send!")

    except Exception as e:
        print(e)
        response = app.response_class(
            response=e, status=400, mimetype="application/json"
        )
    return response


@app.route("/callback", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response_content = ""
    user_message = event.message.text
    group_list = get_group_list()

    if user_message[0:1] == "@":
        if isinstance(event.source, SourceGroup):
            room = next(
                room for room in group_list if room["room_id"] == event.source.group_id
            )
            print(room)
            if room["region"] == "jp":
                response_content = command.find_command(user_message)
                print("jp room")
            else:
                response_content = command.find_command_kr(user_message)
                print("kr room")
        else:
            response_content = command.find_command_kr(user_message)
            print("no data group")

        # 텍스트 메세지면 except로 출력
        try:
            line_bot_api.reply_message(event.reply_token, messages=response_content)
        except Exception as ex:
            print(ex)
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=response_content)
            )

    elif user_message[0:1] == "!":
        user_message = user_message[1:]
        response_content = search.search_db(user_message)

        if response_content is None:
            return

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="현재 ET " + get_eorzea_time() + "\n\n" + response_content
            ),
        )

    elif user_message == "bye":
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Leaving group")
            )
            line_bot_api.leave_group(event.source.group_id)
            print(event.source.group_id, SourceGroup)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Leaving room")
            )
            line_bot_api.leave_room(event.source.room_id)
            print(event.source.room_id, SourceRoom)
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Bot can't leave from 1:1 chat")
            )

    # 글로벌 서버 전환
    elif user_message == "For this journey's end is but one step forward to tomorrow":
        if isinstance(event.source, SourceGroup):
            switch_server("group", event.source.group_id, "jp")
        if isinstance(event.source, SourceRoom):
            switch_server("room", event.source.room_id, "jp")

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="글로벌 서버 채팅방으로 전환합니다.")
        )

    # 한국 서버 전환
    elif user_message == "최팀장 꽃미남":
        if isinstance(event.source, SourceGroup):
            switch_server("group", event.source.group_id, "kr")
        if isinstance(event.source, SourceRoom):
            switch_server("room", event.source.room_id, "kr")

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="한국 서버 채팅방으로 전환합니다.")
        )

    # toy
    elif user_message == "오메가 오메가":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="오메가 오메가"))

    elif "요시다" in user_message:
        pick_yoshida = YOSHIDA[randint(0, 3)]
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=pick_yoshida)
        )


def switch_server(source, id, region):
    with MongoClient(os.getenv("MONGO_URL")):
        db = MongoClient(os.getenv("MONGO_URL")).tweetify
        db.users.update_one(
            {"room_id": id},
            {"$set": {"region": region, "source": source}},
            upsert=True,
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
