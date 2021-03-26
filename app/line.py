
import yaml

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, PostbackEvent, TextMessage, TextSendMessage,
    TemplateSendMessage, ButtonsTemplate, URIAction
)

from Capture import Capture
from SendAnywhereUpload import Upload

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


@handler.add(PostbackEvent)
def handle_postback(event):
    print("INFO: PostbackEvent handle called")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("録画スタートのリクエストを受けました"))
    twitch_user = event.postback.data
    print("event.source: " + event.source)
    message = _capture_upload_create_message(twitch_user)
    line_bot_api.push_message(event.source.userId, message)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("INFO: MessageEvent from " + event.source.user + " handle called")
    print(event.source.userId)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage("録画スタートのリクエストを受けました"))
    twitch_user = event.message.text
    print("event.source.user_id: " + event.source.user_id)
    message = _capture_upload_create_message(twitch_user)
    line_bot_api.push_message(event.source.userId, message)


def make_button_template(link):
    message_template = TemplateSendMessage(
        alt_text="10分以内にダウンロードしてください",
        template=ButtonsTemplate(
            text="10分でリンクが無効になります、すぐにダウンロードしてください。" +
                 "一度しかダウンロード出来ません。",
            title="動画が準備できました！",
            image_size="cover",
            actions=[
                URIAction(
                    uri=link,
                    label="動画をダウンロード"
                )
            ]
        )
    )
    return message_template


def _capture_upload_create_message(twitch_user):
    print("INFO: Twitch User sent in user message: " + twitch_user)
    capture = Capture()
    successful = capture.record(twitch_user)
    if successful:
        filename = capture.get_file_name()
        link = Upload().upload(filename) + "&openExternalBrowser=1"
        return make_button_template(link)
    else:
        print("INFO: Notifying stream recording failure to line user.")
        text = "録画に失敗しました。ストリーミングが見つかりませんでした。後でリトライしてください。"
        return TextSendMessage(text=text)


if __name__ == "__main__":
    _capture_upload_create_message("insomniac")
