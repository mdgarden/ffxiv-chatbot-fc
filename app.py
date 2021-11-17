import os
import sys

from flask import Flask, request, abort

from dotenv import load_dotenv
from src.command import find_command, find_command_kr
from src.search import search_db
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    SourceGroup,
    SourceRoom,
)

# take environment variables from .env
load_dotenv()

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET")
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
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


isSpoilerRoom = []


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    response_content = ""
    user_message = event.message.text

    if user_message[0:1] == "@":
        if isinstance(event.source, SourceGroup):
            if event.source.group_id in isSpoilerRoom:
                response_content = find_command(user_message)
            else:
                response_content = find_command_kr(user_message)

        try:
            line_bot_api.reply_message(event.reply_token, messages=response_content)
        except Exception as ex:
            print(ex)

    elif user_message[0:1] == "!":
        user_message = user_message[1:]
        response_content = search_db(user_message)
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=response_content)
        )

    elif user_message == "bye":
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Leaving group")
            )
            line_bot_api.leave_group(event.source.group_id)
            print(event.source, SourceGroup)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Leaving group")
            )
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="Bot can't leave from 1:1 chat")
            )

    elif user_message == "I close my eyes, tell us why must we suffer":
        if isinstance(event.source, SourceGroup):
            if event.source.group_id in isSpoilerRoom:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="한국 서버로 설정되어있습니다.")
                )
            else:
                isSpoilerRoom.append(event.source.group_id)
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="한국 서버 그룹으로 전환합니다.")
                )
        if isinstance(event.source, SourceRoom):
            if event.source.room_id in isSpoilerRoom:
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="한국 서버로 설정되어있습니다.")
                )
            else:
                isSpoilerRoom.append(event.source.room_id)
                line_bot_api.reply_message(
                    event.reply_token, TextSendMessage(text="한국 서버 룸으로 전환합니다.")
                )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)

# 지하실 event.source, SourceGroup{"groupId": "Cda4a62dd237e6d8099314e83dc25afd9", "type": "group", "userId": "Uc81077b9c8d2fd8840b86b2dc0990062"} <class 'linebot.models.sources.SourceGroup'>
