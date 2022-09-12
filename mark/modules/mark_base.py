# Copyright (c) 2021 Itz-fork

from asyncio import sleep
from random import choice
from heroku3 import from_key
from pyrogram import enums

from Mark.data.mark_msgs import Emergency_Msgs, Photo_Reesponse, Sticker_Response, Video_and_gif_Response, Document_Response
from Mark.data.database import Mark_Database
from Mark.data.defaults import Defaults
from .openai_mark import Mark_OpenAI
from .arq_mark import Mark_ARQ
from .affiliateplus_mark import Mark_Affiliate
from config import Config


class Mark_Base():
    """
    Base of Mark Chat bot
    """

    def __init__(self) -> None:
        if Config.ON_HEROKU:
            heroku_c = from_key(Config.HEROKU_API)
            self.heroku_app = heroku_c.app(Config.HEROKU_APP_NAME)
        else:
            self.heroku_app = None
            self.mark_sql_db = Mark_Database()

    async def get_answer_from_mark(self, quiz, usr_id):
        ai_engine = await self.get_ai_engine()
        try:
            mark_oai = Mark_OpenAI(ai_engine)
            # Get old / new chat log
            c_log = await mark_oai.get_chat_log(usr_id)
            # Asks quistion from mark (OpenAI)
            answ = await mark_oai.ask_mark(quiz, c_log)
            # Save the chat log of the user
            await mark_oai.append_and_save_chat_log(quiz, answ, usr_id, c_log)
            return answ
        except Exception as e:
            print(e)
            try:
                if Config.DEFAULT_CHATBOT == "affiliateplus":
                    mark_af = Mark_Affiliate()
                    return await mark_af.ask_mark(quiz, usr_id)
                else:
                    mark_luna = Mark_ARQ(Config.ARQ_API_URL, Config.ARQ_KEY)
                # Asks question from Mark (Luna chat bot)
                return await mark_luna.ask_mark(quiz, usr_id)
            except:
                return await self.emergency_pick()

    async def reply_to_user(self, message, answer):
        chat_id = message.chat.id
        await message.reply_chat_action(enums.ChatAction.TYPING)
        # Sleeping for 2 seconds to make the bot more real
        await sleep(2)
        await message.reply_text(answer, reply_to_message_id=message.id)

    async def set_ai_engine(self, engine):
        if self.heroku_app:
            conf = self.heroku_app.config()
            conf["ENGINE"] = str(engine)
        else:
            await self.mark_sql_db.set_engine(engine)

    async def get_ai_engine(self):
        if self.heroku_app:
            conf = self.heroku_app.config()
            try:
                if conf["ENGINE"]:
                    return conf["ENGINE"]
                else:
                    return Defaults().Engine
            except:
                return Defaults().Engine
        else:
            engine = await self.mark_sql_db.get_engine()
            if not engine:
                return Defaults().Engine
            else:
                return engine

    async def restart_mark(self):
        try:
            if self.heroku_app:
                self.heroku_app.restart()
            else:
                return
        except Exception as e:
            print(f"Error: {e}")

    async def emergency_pick(self):
        return choice(Emergency_Msgs)

    async def image_resp(self):
        return choice(Photo_Reesponse)

    async def vid_resp(self):
        return choice(Video_and_gif_Response)

    async def doc_resp(self):
        return choice(Document_Response)

    async def sticker_resp(self):
        return choice(Sticker_Response)
