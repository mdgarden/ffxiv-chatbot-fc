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
    JoinEvent,
    TextMessage,
    TextSendMessage,
    SourceGroup,
    SourceRoom,
)

# get environment variables from .env
load_dotenv()
app = Flask(__name__)


def get_room_list():
    with MongoClient(os.getenv("MONGO_URL")):
        db = MongoClient(os.getenv("MONGO_URL")).tweetify
        room_list = list(db.users.find())
    return room_list


def get_room_type(event):
    if isinstance(event.source, SourceGroup):
        sender_id = {"type": event.source.type, "group_id": event.source.group_id}
    elif isinstance(event.source, SourceRoom):
        sender_id = {"type": event.source.type, "room_id": event.source.room_id}
    else:
        sender_id = {"type": event.source.type, "user_id": event.source.user_id}
    return sender_id


def get_room_region(event):
    room_list = get_room_list()
    # TODO: find room by value(user_id)
    if isinstance(event.source, SourceGroup):
        for room in room_list:
            try:
                if room["group_id"] == event.source.group_id:
                    return room["region"]
            except Exception as e:
                print("this instance is not group")
                print(e)
    elif isinstance(event.source, SourceRoom):
        for room in room_list:
            try:
                if room["room_id"] == event.source.room_id:
                    return room["region"]
            except Exception as e:
                print("this instance is not room")
                print(e)
    else:
        for room in room_list:
            try:
                if room["user_id"] == event.source.user_id:
                    return room["region"]
            except Exception as e:
                print("this instance is not 1:1")
                print(e)


def update_region(event, region):
    sender_id = get_room_type(event)
    with MongoClient(os.getenv("MONGO_URL")):
        db = MongoClient(os.getenv("MONGO_URL")).tweetify
        db.users.update_one(
            sender_id,
            {"$set": {"status": os.getenv("STATUS"), "region": region}},
            upsert=True,
        )


def leave_group(event):
    if isinstance(event.source, SourceGroup):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="Leaving group")
        )
        line_bot_api.leave_group(event.source.group_id)
    elif isinstance(event.source, SourceRoom):
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="Leaving room")
        )
        line_bot_api.leave_room(event.source.room_id)
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="Bot can't leave from 1:1 chat")
        )


def delete_room(event):
    sender_id = get_room_type(event)

    with MongoClient(os.getenv("MONGO_URL")):
        db = MongoClient(os.getenv("MONGO_URL")).tweetify
        db.users.update_one(
            sender_id,
            {"$set": {"status": "leave", "region": "kr"}},
            upsert=True,
        )


def reply_static_message(message):
    YOSHIDA = ["요시다아아아아", "요시다!!!!!", "요시다?", "요시다...."]
    if "요시다" in message:
        return TextSendMessage(text=YOSHIDA[randint(0, 3)])
    if message == "오메가 오메가":
        return TextSendMessage(text=message)


def send_message(event, message):
    # message should formatted (require type)
    # https://developers.line.biz/en/reference/messaging-api/#messages
    line_bot_api.reply_message(event.reply_token, messages=message)


room_list = get_room_list()


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

room_list = get_room_list()


@app.route("/")
def hello_world():
    return "Application is Running!"


@app.route("/tweet", methods=["POST"])
def send_new_tweet():
    body = request.get_data(as_text=True)
    response = app.response_class(
        response=json.dumps(body), status=200, mimetype="application/json"
    )
    data = json.loads(body)

    try:
        for group in room_list:
            if (
                group["status"] == os.getenv("STATUS")
                and group["region"] == data["region"]
            ):
                line_bot_api.push_message(
                    group["group_id"], [TextSendMessage(text=data["text"])]
                )
                line_bot_api.push_message(
                    group["group_id"], [TextSendMessage(text=data["link"])]
                )

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


@handler.add(JoinEvent)
def handle_join(event):
    update_region(event, "kr")
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="타타루에용! 잘 부탁드립니당!")
    )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    response_content = ""
    region = ""

    try:
        region = get_room_region(event)
        print("region")
        print(region)
    except Exception as e:
        update_region(event, "kr")
        region = get_room_region(event)
        print("not found region")
        print(e)

    # command
    if user_message[0:1] == "@":
        response_content = command.find_command(region, user_message)
    elif user_message[0:1] == "!":
        response_content = search.search_db(user_message[1:])

    # quick reply
    elif "요시다" in user_message or user_message == "오메가 오메가":
        response_content = reply_static_message(user_message)

    # switch server
    elif user_message == "For this journey's end is but one step forward to tomorrow":
        update_region(event, "jp")
        response_content = TextSendMessage(text="글로벌 서버의 정보를 알려드려용!")
    elif user_message == "바나나 받아라 타이탄":
        update_region(event, "kr")
        response_content = TextSendMessage(text="한국 서버의 정보를 알려드려용!")

    # leave group
    elif user_message == "bye":
        delete_room(event)
        leave_group(event)
    else:
        return

    if response_content is None:
        return
    if response_content is not None:
        send_message(event, response_content)


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
