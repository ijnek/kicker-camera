
import threading
import os
import time
import tracemalloc
import linecache

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

channel_access_token = os.environ['LINE_BOT_CHANNEL_TOKEN']
channel_secret = os.environ['LINE_BOT_CHANNEL_SECRET']
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

tracemalloc.start()


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
    user_id = event.source.user_id
    print("INFO: Handle for PostbackEvent called from user_id " + user_id)

    twitch_user = event.postback.data
    threading.Thread(
        target=capture_upload_push_message,
        args=(twitch_user, user_id)).start()

    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    print("INFO: Handle for MessageEvent called from user_id " + user_id)

    twitch_user = event.message.text
    threading.Thread(
        target=capture_upload_push_message,
        args=(twitch_user, user_id)).start()


def make_button_template(link):
    message_template = TemplateSendMessage(
        alt_text="動画が届きました！",
        template=ButtonsTemplate(
            text="リンクは一度かぎり有効で、10分で無効になります。",
            title="「ダウンロード」を選択してください",
            image_size="cover",
            actions=[
                URIAction(
                    uri=link,
                    label="動画を見る"
                )
            ]
        )
    )
    return message_template


def capture_upload_create_message(twitch_user):
    print("INFO: Twitch User sent in user message: " + twitch_user)
    capture = Capture()
    successful = capture.record(twitch_user)

    return None

    # if successful:
    #     filename = capture.get_file_name()
    #     link = Upload().upload(filename) + "&openExternalBrowser=1"
    #     return make_button_template(link)
    # else:
    #     print("INFO: Notifying stream recording failure to line user.")
    #     text = "録画に失敗しました。カメラを検出出来ません。後でリトライしてください。"
    #     return TextSendMessage(text=text)


def capture_upload_push_message(twitch_user, user_id):
    message = capture_upload_create_message(twitch_user)
    # line_bot_api.push_message(user_id, message)


def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


if __name__ == "__main__":

    tracemalloc.start()

    capture_upload_create_message("insomniac")

    for _ in range(20):
        threading.Thread(
            target=capture_upload_create_message,
            args=("insomniac",)).start()
        time.sleep(1)

    time.sleep(10)

    snapshot = tracemalloc.take_snapshot()
    display_top(snapshot)

    time.sleep(1000)
