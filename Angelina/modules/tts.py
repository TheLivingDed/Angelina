from telegram import ChatAction
from gtts import gTTS
import html
import urllib.request
import re
import json
from datetime import datetime
from typing import Optional, List
import time
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from Angelina import dispatcher
from Angelina.__main__ import STATS
from Angelina.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from Angelina.modules.helper_funcs.extraction import extract_user

def speak(bot: Bot, update: Update, args):
    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    reply = " ".join(args)
    update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    lang="ml"
    speak = gTTS(reply, lang)
    speak.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "en"
        speak = gTTS(reply, lang)
        speak.save("k.mp3")
    with open("k.mp3", "rb") as speech:
        update.message.reply_voice(speech, quote=False)

__mod_name__ = "Text To Speech"

AFK_REGEX_HANDLER = DisableAbleRegexHandler("(?i)speak", speak, friendly="speak")

dispatcher.add_handler(CommandHandler('speak', speak, pass_args=True))
dispatcher.add_handler(AFK_REGEX_HANDLER)

