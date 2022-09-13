# Copyright (c) 2022 laurence mark

import re

from pyrogram import Client as markai, filters, enums
from pyrogram.types import Message
from mark.data.defaults import Defaults
from mark_base import Mark_Base
from config import Config


# Bot Id
mark_bot_id = int(Config.BOT_TOKEN.split(":")[0])


# Chat
@markai.on_message(~filters.command(["engine", "help", "restart"]) &~filters.via_bot)
async def talk_with_mark(_, message: Message):
    c_type = message.chat.type
    r_msg = message.reply_to_message
    mark_base = Mark_Base()
    # For Private chats
    if c_type == enums.ChatType.PRIVATE:
        quiz_text = message.text
    # For Public and private groups
    elif c_type == enums.ChatType.SUPERGROUP or enums.ChatType.GROUP:
        # Regex to find if "mark" or "Mark" in the message text
        if message.text and re.search(f"{Config.CHAT_BOT_NAME}|{Config.CHAT_BOT_NAME.upper()}|{Config.CHAT_BOT_NAME.lower()}", message.text):
            quiz_text = message.text
        # For replied message
        elif r_msg:
            if not r_msg.from_user:
                return
            # If replied message wasn't sent by the bot itself won't be answered
            if r_msg.from_user.id == mark_bot_id:
                quiz_text = None
                if message.text:
                    quiz_text = message.text
            else:
                return
        else:
            return await message.stop_propagation()
    else:
        return await message.stop_propagation()
    # Arguments
    if quiz_text:
        quiz = quiz_text.strip()
    else:
        if message.photo:
            return await mark_base.reply_to_user(message, await mark_base.image_resp())
        elif message.video or message.video_note or message.animation:
            return await mark_base.reply_to_user(message, await mark_base.vid_resp())
        elif message.document:
            return await mark_base.reply_to_user(message, await mark_base.doc_resp())
        elif message.sticker:
            return await mark_base.reply_to_user(message, await mark_base.sticker_resp())
        else:
            return await message.stop_propagation()
    usr_id = message.from_user.id
    # Get the reply from Mark
    rply = await mark_base.get_answer_from_mark(quiz, usr_id)
    await mark_base.reply_to_user(message, rply)


# Set AI Engine (For OpenAI)
@markai.on_message(filters.command("engine") & filters.user(Config.OWNER_ID))
async def set_mark_engine(_, message: Message):
    if len(message.command) != 2:
        engines_txt = """
**⚡️ OpenAI Engines**


**Base**

✧ `davinci` - The most capable engine and can perform any task the other models can perform and often with less instruction.
✧ `curie` - Extremely powerful, yet very fast.
✧ `babbage` - Can perform straightforward tasks like simple classification.
✧ `ada` - Usually the fastest model and can perform tasks that don’t require too much nuance.


**GPT-3 Models**

GPT-3 models can understand and generate natural language. Openai offer four main models with different levels of power suitable for different tasks. Davinci is the most capable model, and Ada is the fastest

✧ `text-davinci-002`
✧ `text-curie-001`
✧ `text-babbage-001`
✧ `text-ada-001`


**👀 How to set the engines?**

To set an engine use `/engine` command followed by the engine code name you want
**Ex:**
`/engine text-curie-001`"""
        return await message.reply_text(engines_txt)
    else:
        mark_base = Mark_Base()
        try:
            selected_engine = message.text.split(None)[1].strip()
            if selected_engine in Defaults().Engines_list:
                await mark_base.set_ai_engine(selected_engine)
                await message.reply(f"**Successfully Changed OpenAI Engine** \n\n**New Engine:** `{selected_engine}`")
            else:
                await message.reply("**Invalid Engine Selected!**")
        except:
            await message.reply(await mark_base.emergency_pick())


# Help
@markai.on_message(filters.command("help"))
async def help_mark(_, message: Message):
    help_msg = """
**✨ Help Section**


**How to change OpenAI engine 🤔?**
    - To change OpenAI Engine use `/engine` command followed by the engine name. For more info send /engine command

**How to ban someone from Bot 🤔?**
    - This is a chat bot tho. Why you need to ban someone? If it's necessary use "banable" branch and send `/ban` command (Only for Heroku Users)


**Made with ❤️ by @NexaBotsUpdates**
"""
    await message.reply(help_msg, reply_to_message_id=message.id)


# Restart Heroku App
@markai.on_message(filters.command("restart"))
async def restart_mark(_, message: Message):
    if Config.ON_HEROKU:
        mark_base = Mark_Base()
        await message.reply(f"`Restarting {Config.CHAT_BOT_NAME}, Please wait...!`")
        await mark_base.restart_mark()
    else:
        await message.reply("**This command is available only for Heroku users**")
