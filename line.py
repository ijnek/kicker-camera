
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
    TemplateSendMessage, ButtonsTemplate, URIAction
)

from Capture import Capture
from Upload import Upload

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

'''
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    filename = Capture('kenjibrameld').record()

    if filename:
        link = Upload().upload(filename)
        text = "動画が準備できました！\n" + link
    else:
        text = "録画に失敗しました。ストリーミングが見つかりませんでした。後でリトライしてください。”

    line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text))
'''

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    messages = make_button_template()
    line_bot_api.reply_message(
        event.reply_token,
        messages
    )

def make_button_template():
    message_template = TemplateSendMessage(
        alt_text="にゃーん",
        template=ButtonsTemplate(
            text="どこに表示されるかな？",
            title="タイトルですよ",
            image_size="cover",
            thumbnail_image_url="https://www.i-sedai.com/pet/column/image/C0108_1.jpg",
            actions=[
                URIAction(
                    uri="https://google.com",
                    label="URIアクションのLABEL"
                )
            ]
        )
    )
    return message_template