import os
import json
import asyncio
import subprocess
import redis
import logging
from yt_dlp import YoutubeDL
from pyrogram import Client, idle, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo
from PHB.database import DB
from config import BOT_USERNAME, BOT, LOGS, OWNER, DUMP_GRP, SPY_GRP


# Some Stuffs
def add_to_db(phid, chatid, msgid, link):
    DB[phid] = f"{chatid},{msgid},{link}"
    
    
@Client.on_callback_query(filters.regex(pattern="ph_(.*)"))
async def ph_dl_video(client, cb):
    phid = cb.matches[0].group(1)
    url = f"https://www.pornhub.com/view_video.php?viewkey={phid}"
    try:
        await cb.edit_message_text("`Downloading...`")
        with YoutubeDL({}) as ydl:
            info = ydl.extract_info(url, download=False)
        gdown = await asyncio.create_subprocess_shell(
            f"yt-dlp {url} --write-thumbnail -o '%(id)s.mp4'",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        while gdown.returncode is None:
            await asyncio.sleep(0.25)
        rip_file = f"{phid}.mp4"
        dir = os.listdir()
        if f"{phid}.jpg" in dir:
            thumb = f"{phid}.jpg"
        elif f"{phid}.png" in dir:
            thumb = f"{phid}.png"
        elif f"{phid}.webp" in dir:
            thumb = f"{phid}.webp"
        else:
            thumb = None
            
    except Exception as yterr:
        print(yterr)
    try:
        await cb.edit_message_text("`Uploading...`")
        msg = await BOT.send_video(chat_id=DUMP_GRP, video=rip_file, duration=info['duration'], thumb=thumb, supports_streaming=True, caption=phid)
        add_to_db(phid, msg.chat.id, msg.message_id, msg.link) 
        await cb.edit_message_media(InputMediaVideo(f"{msg.video.file_id}", caption=url))
        await BOT.send_message(chat_id=SPY_GRP, text=f"{msg.link} \nRequested by - {cb.from_user.mention}", disable_web_page_preview=True)
    except Exception as downerr:
        await cb.edit_message_text(f"**ERROR ⚠️** \n`{downerr}`")
    try:
        os.system(f"rm {rip_file}")
    except:
        pass
    
    
