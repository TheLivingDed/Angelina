#Modificatins by anonyindian
import html
import json
import os
import psutil
import random
import time
import datetime
from typing import Optional, List
import re
import requests
from telegram.error import BadRequest
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html
from Angelina.modules.helper_funcs.chat_status import user_admin, sudo_plus, is_user_admin
from Angelina import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, DEV_USERS, WHITELIST_USERS
from Angelina.__main__ import STATS, USER_INFO, TOKEN
from Angelina.modules.disable import DisableAbleCommandHandler, DisableAbleRegexHandler
from Angelina.modules.helper_funcs.extraction import extract_user
from Angelina.modules.helper_funcs.filters import CustomFilters
import Angelina.modules.sql.users_sql as sql
import Angelina.modules.helper_funcs.cas_api as cas

@run_async
def info(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    chat = update.effective_chat
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not message.reply_to_message and not args:
        user = message.from_user

    elif not message.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not message.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        message.reply_text("I can't extract a user from this.")
        return

    else:
        return
    
    text = (f"<b>User Information:</b>\n"
            f"🆔: <code>{user.id}</code>\n"
            f"👤Name: {html.escape(user.first_name)}")

    if user.last_name:
        text += f"\n🚹Last Name: {html.escape(user.last_name)}"

    if user.username:
        text += f"\n♻️Username: @{html.escape(user.username)}"

    text += f"\n☣️Permanent user link: {mention_html(user.id, 'link🚪')}"

    num_chats = sql.get_user_num_chats(user.id)
    text += f"\n🌐Chat count: <code>{num_chats}</code>"
    text += "\n🎭Number of profile pics: {}".format(bot.get_user_profile_photos(user.id).total_count)
   
    try:
        user_member = chat.get_member(user.id)
        if user_member.status == 'administrator':
            result = requests.post(f"https://api.telegram.org/bot{TOKEN}/getChatMember?chat_id={chat.id}&user_id={user.id}")
            result = result.json()["result"]
            if "custom_title" in result.keys():
                custom_title = result['custom_title']
                text += f"\n🛡This user holds the title⚜️ <b>{custom_title}</b> here."
    except BadRequest:
        pass

   

    if user.id == OWNER_ID:
        text += "\n🚶🏻‍♂️Sed, He is my Owner🤴\nI will ban you, If I came to know that you doing things against him.😒"
        
    elif user.id in DEV_USERS:
        text += "\n🚴‍♂️With His Limitless Power This User is a *Apologypse*!."
        
    elif user.id in SUDO_USERS:
        text += "\nWith His Limited Power This User is a *Scorpion*" \
                    "Not Powerful as Apologypse But Still watch it.."
        
    elif user.id in SUPPORT_USERS:
        text += "\n🚴‍♂️With His Single Power This User is a *Mortal*! " \
                        "Not quite a Scorpion user, but can still gban you off the map."
        
  
       
    elif user.id in WHITELIST_USERS:
        text += "\nWith His Ability This User Knight! " \
                        "That means I'm not allowed to ban/kick them."
    elif user.id == bot.id:     
        text += "\n💃Lol🧞‍♂️It's Me, Your Loving One *Angelina*😉"


    text +="\n"
    text += "\nCAS banned: "
    result = cas.banchecker(user.id)
    text += str(result)
    for mod in USER_INFO:
        if mod.__mod_name__ == "Users":
            continue

        try:
            mod_info = mod.__user_info__(user.id)
        except TypeError:
            mod_info = mod.__user_info__(user.id, chat.id)
        if mod_info:
            text += "\n" + mod_info
    try:
        profile = bot.get_user_profile_photos(user.id).photos[0][-1]
        bot.sendChatAction(chat.id, "upload_photo")
        bot.send_photo(chat.id, photo=profile, caption=(text), parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except IndexError:
        update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

INFO_HANDLER = DisableAbleCommandHandler(["info", "whois"],  info, pass_args=True)
dispatcher.add_handler(INFO_HANDLER)
