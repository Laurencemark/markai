# Copyright (c) 2022 laurence mark

from pyrogram import Client
from config import Config

yuiai = Client(
    "YuiChatBot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="mark/modules")
)