
import yaml

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from capture import record
from upload import upload

app = Flask(__name__)

yaml_file = open("application.yml", 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)

channel_access_token = yaml_content.get('line.bot').get('channel-token')
channel_secret = yaml_content.get('line.bot').get('channel-secret')
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    filename = record()

    if filename:
        link = upload(filename)
        text = link
    else:
        text = "Could not locate stream. Please ensure the stream is up and running."

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))