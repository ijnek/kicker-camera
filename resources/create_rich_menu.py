import os
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, \
    RichMenuBounds, PostbackAction
from linebot import LineBotApi

channel_access_token = os.environ['LINE_BOT_CHANNEL_TOKEN']
channel_secret = os.environ['LINE_BOT_CHANNEL_SECRET']
twitch_username = os.environ['TWITCH_USERNAME']

line_bot_api = LineBotApi(channel_access_token)

display_text = "録画始まりました、どうぞ滑ってください！"

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1162),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="録画ボタン",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=2500, height=1408),
        action=PostbackAction(data=twitch_username,
                              display_text=display_text))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

with open("record_button.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

line_bot_api.set_default_rich_menu(rich_menu_id)
