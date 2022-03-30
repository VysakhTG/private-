import os
import asyncio
import redis
import logging
import json
from pornhub_api import PornhubApi
from pyrogram import Client, idle, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaAudio, InputMediaVideo, InlineQuery, InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InputTextMessageContent
from config import BOT_USERNAME, BOT, LOGS, OWNER, DUMP_GRP
from src.database import DB

# Some Stuffs 
def check_user(id):
    hola = DB["USERS"].split(" ")
    if str(id) in hola:
        pass
    else:
        DB.append("USERS", f" {id}")
        
ph = PornhubApi()


# Main Inline Syntax
@Client.on_inline_query()
async def inline_query_handler(client, iquery: InlineQuery):
    answers = []
    text = iquery.query.lower()
    check_user(iquery.from_user.id)
    if text == "":
        answers.append(
            InlineQueryResultArticle(
                title="Search...",
                description=f"@{BOT_USERNAME} [search]",
                thumb_url="https://i.pcmag.com/imagery/articles/07hppU34PuukyCinq2uoG4K-1..v1569491125.jpg",
                input_message_content=InputTextMessageContent(message_text=f"**Search Something...** \nEx:-  `@{BOT_USERNAME} Dani Daniels`")
            )
        )
        await iquery.answer(cache_time=0, results=answers, switch_pm_text="Search...", switch_pm_parameter="start")
    else:
        try:
            vids = ph.search.search(text)
            for vid in vids.videos:
                PS = []
                name = vid.title
                thumb = vid.thumb
                url = vid.url
                id = vid.video_id
                
                for x in vid.pornstars:
                    PS.append(x.pornstar_name)
                artists = ", ".join(PS)
                desc = f"{vid.duration} | {vid.views} Views | {artists}"
                caption = f"[{name}]({url}) \n({artists})"
                data = DB.get(id)
                if data:
                    answers.append(
                        InlineQueryResultVideo(
                            video_url=data.split(",")[2],
                            title=name,
                            description=desc,
                            thumb_url=thumb,
                            caption=caption
                        )
                    )
                else:
                    answers.append(
                        InlineQueryResultPhoto(
                            photo_url=thumb, 
                            title=name, 
                            description=desc, 
                            caption=caption, 
                            reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Get ⬇️",
                                            callback_data=f"ph_{id}"
                                        )    
                                    ]
                                ]
                            ),
                        )
                    )
            await iquery.answer(cache_time=0, results=answers)
        except Exception as ep:
            answers.append(
                InlineQueryResultArticle(
                    title="ERROR",
                    input_message_content=InputTextMessageContent(message_text=f"**ERROR ⚠️** \n`{ep}`")
                )
            )
            await iquery.answer(cache_time=0, results=answers)
            print(ep)
            pass
                
