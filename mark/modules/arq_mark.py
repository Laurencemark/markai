# Copyright (c) 2022 laurence mark

from aiohttp import ClientSession
from Python_ARQ import ARQ
from config import Config


class Mark_ARQ():
    """
    ARQ Class of Mark AI

    Methods:
        __close_session - Closes the aiohttp session
        ask_mark - Get response from luna chat bot
    """

    def __init__(self, api, key) -> None:
        self.session = ClientSession()
        self.arq = ARQ(api, key, self.session)

    async def __close_session(self, aiohtp_c):
        await aiohtp_c.close()

    async def ask_mark(self, question, user_id):
        frm_luna = await self.arq.luna(question, user_id)
        await self.__close_session(self.session)
        if frm_luna.ok:
            return f"{frm_luna.result}".replace("Luna", Config.CHAT_BOT_NAME)
        else:
            return None
