import os
import sys
from pyrogram import Client, idle, filters
from pyrogram.types import Message
from PHB.database import DB
from config import LOGS, BOT, DUMP_GRP, OWNER

@Client.on_message(filters.command("addkey") & filters.user(OWNER))
async def addkey(client, m: Message):
    if len(m.command) < 3:
        await m.reply("`/addkey [KEY_NAME] [KEY_VALUE]`")
    else:
        hmm = m.text.split(None, 1)[1]
        key = hmm.split(None, 1)[0]
        value = hmm.split(None, 1)[1]
        try:
            DB[key] = value
            await m.reply(f'**Key Added Successfully!** \n**KEY** - `{key}` \n**VALUE** - `{value}`')
        except Exception as e:
            await m.reply(f"`{e}`")
            
@Client.on_message(filters.command("getkey") & filters.user(OWNER))
async def getkey(client, m: Message):
    if len(m.command) != 2:
        await m.reply("`/getkey [KEY_NAME]`")
    else:
        try:
            value = DB[m.text.split(" ")[1]]
            await m.reply(f'**KEY** - `{m.text.split(" ")[1]}` \n**VALUE** - `{value}`')
        except Exception as e:
            await m.reply(f'No Key named - `{m.text.split(" ")[1]}` was found.')
            
@Client.on_message(filters.command("delkey") & filters.user(OWNER))
async def delkey(client, m: Message):
    if len(m.command) != 2:
        await m.reply("`/delkey [KEY_NAME]`")
    else:
        key = DB[m.text.split(" ")[1]]
        k = DB.delete(key)
        if k == 0:
            await m.reply(f'No Key named - `{m.text.split(" ")[1]}` was found.')
        else:
            await m.reply(f'**Key Deleted** - `{m.text.split(" ")[1]}`') 
            
@Client.on_message(filters.command("getall") & filters.user(OWNER))
async def getall(client, m: Message):
    await m.reply(f"`{DB.keys()}`")

@Client.on_message(filters.command("addsudo") & filters.user(OWNER))
async def addsudo(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        await m.reply("Reply to A User :/")
    else:
        sid = replied.from_user.id
        if str(sid) in DB["SUDOS"].split(" "):
            await m.reply(f"`{sid}` is already a Sudo User")
        else:
            DB.append("SUDOS", f" {sid}")
            await replied.reply(f"Added `{sid}` to Sudo")

@Client.on_message(filters.command("delsudo") & filters.user(OWNER))
async def delsudo(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        await m.reply("Reply to A User :/")
    else:
        sid = replied.from_user.id
        if str(sid) in DB["SUDOS"].split(" "):
            haha = DB["SUDOS"].split(" ")
            haha.remove(str(sid))
            DB["SUDOS"] = " ".join(haha)
            await replied.reply(f"Removed `{sid}` from Sudo")
        else:
            await m.reply(f"`{sid}` is not a Sudo User")
    
@Client.on_message(filters.command("restart") & filters.user(OWNER))
async def restart(client, m: Message):
    await m.reply("Restarting...")
    os.execl(sys.executable, sys.executable, *sys.argv)
    # You probably don't need it but whatever
    quit()

  
