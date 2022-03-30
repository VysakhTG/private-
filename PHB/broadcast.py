import os
from pyrogram import Client, idle, filters
from pyrogram.types import Message
from PHB.database import DB, sudo_filter
from config import LOGS, BOT, OWNER


@Client.on_message(sudo_filter & filters.command('broadcast'))
async def bc(client, m: Message):
    if len(m.command) < 2:
        await m.reply("Give something to Broadcast...")
    else:
        status = await m.reply("`Broadcasting...`")
        P = 0
        F = 0
        msg = m.text.split(" ", maxsplit=1)[1]
        for usr in DB['USERS'].split(" "):
            try:
                await BOT.send_message(int(usr), msg)
                P += 1
            except:
                F += 1
                pass
        await status.edit(f"**Broadcast Complete ✅** \nBroadcasted in `{P}` chats, `{F}` failed.")
