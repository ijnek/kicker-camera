import yaml
from linebot.models import RichMenu, RichMenuSize, RichMenuArea, \
    RichMenuBounds, PostbackAction
from linebot import LineBotApi

yaml_file = open("../application.yml", 'r')
yaml_content = yaml.load(yaml_file, Loader=yaml.FullLoader)

channel_access_token = yaml_content.get('line.bot').get('channel-token')
channel_secret = yaml_content.get('line.bot').get('channel-secret')
line_bot_api = LineBotApi(channel_access_token)

rich_menu_to_create = RichMenu(
    size=RichMenuSize(width=2500, height=1408),
    selected=False,
    name="Nice richmenu",
    chat_bar_text="録画ボタン",
    areas=[RichMenuArea(
        bounds=RichMenuBounds(x=0, y=0, width=2500, height=1408),
        action=PostbackAction(data="kenjibrameld", 
                              display_text="録画スタートをリクエストしました"))]
)
rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

with open("record_button.png", 'rb') as f:
    line_bot_api.set_rich_menu_image(rich_menu_id, 'image/png', f)

line_bot_api.set_default_rich_menu(rich_menu_id)
