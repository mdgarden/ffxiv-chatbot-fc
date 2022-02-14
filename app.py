import os
from random import randint
import sys

from flask import Flask, request, abort

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

isNoSpoilerRoom = [
    "Cda4a62dd237e6d8099314e83dc25afd9",
    "C4164d10181925811417349e3b563ea3f",
]

isSpoilerRoom = []

YOSHIDA = ["요시다아아아아", "요시다!!!!!", "요시다?", "요시다...."]

# Run get_new_tweet()

# take environment variables from .env
load_dotenv()

app = Flask(__name__)

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

    if user_message[0:1] == "@":
        if isinstance(event.source, SourceGroup):
            if event.source.group_id in isNoSpoilerRoom:
                response_content = command.find_command_kr(user_message)
            else:
                response_content = command.find_command(user_message)
        else:
            response_content = command.find_command(user_message)

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

    elif "요시다" in user_message:
        pick_yoshida = YOSHIDA[randint(0, 3)]
        print(pick_yoshida)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=pick_yoshida)
        )

    # 한국 서버 전환
    # elif user_message == "선대 아젬 베네스":
    #     print("venat")
    #     if isinstance(event.source, SourceGroup):
    #         if event.source.group_id not in isNoSpoilerRoom:
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="글로벌 서버로 설정되어있습니다.")
    #             )
    #             print(isNoSpoilerRoom)
    #         else:
    #             isNoSpoilerRoom.append(event.source.group_id)
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="한국 서버 그룹으로 전환합니다.")
    #             )
    #             print(isNoSpoilerRoom)
    #     if isinstance(event.source, SourceRoom):
    #         if event.source.room_id in isNoSpoilerRoom:
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="한국 서버로 설정되어있습니다.")
    #             )
    #             print(isNoSpoilerRoom)
    #         else:
    #             isNoSpoilerRoom.append(event.source.room_id)
    #             line_bot_api.reply_message(
    #                 event.reply_token, TextSendMessage(text="한국 서버 룸으로 전환합니다.")
    #             )
    #             print(isNoSpoilerRoom)

    elif user_message == "오메가 오메가":
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="오메가 오메가"))


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
