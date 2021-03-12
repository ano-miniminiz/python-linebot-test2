import os
from linebot import (
    LineBotApi, WebhookHandler
)
from main import line_bot_api

from linebot.models import (
    RichMenu, RichMenuSize, RichMenuArea, RichMenuBounds, MessageAction
)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)



rich_menu_to_create = RichMenu(
    size = RichMenuSize(width=1200, height=405),
    selected = True,
    name = 'richmenu for randomchat',
    hat_bar_text = 'TAP HERE',
    areas=[
        RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=480, height=405),
            action=MessageAction(text="やかましいわ！")
        ),
        RichMenuArea(
            bounds=RichMenuBounds(x=480, y=0, width=720, height=405),
            action=MessageAction(text="あら")
        )
    ]
)
richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

# upload an image for rich menu
path = 'gude.jpg'

with open(path, 'rb') as f:
    line_bot_api.set_rich_menu_image(richMenuId, "image/jpeg", f)

# set the default rich menu
line_bot_api.set_default_rich_menu(richMenuId)

