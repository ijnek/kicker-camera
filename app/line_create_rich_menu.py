import os
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, \
    RichMenuBounds, PostbackAction
from linebot import LineBotApi

# Creates and pushes a LINE rich menu for the messaging API

channel_access_token = os.environ['LINE_BOT_CHANNEL_TOKEN']
channel_secret = os.environ['LINE_BOT_CHANNEL_SECRET']
twitch_username = os.environ['TWITCH_USERNAME']
capture_seconds = os.getenv('CAPTURE_SECONDS', 60)


def create_rich_menu():

    print("INFO: Creating rich menu")

    line_bot_api = LineBotApi(channel_access_token)

    print("1")

    display_text = str(capture_seconds) + "秒の録画が始まりました！\nスマホをしまっても大丈夫です"

    print("2")

    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=2500, height=1204),
        selected=True,
        name="Nice richmenu",
        chat_bar_text="録画ボタン",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1408),
            action=PostbackAction(data=twitch_username,
                                  display_text=display_text))]
    )

    print("3")

    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

    print("4")

    with open("resources/record_button.png", 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

    print("5")

    line_bot_api.set_default_rich_menu(rich_menu_id)

    print("INFO: Finished creating rich menu")


if __name__ == "__main__":
    create_rich_menu()
