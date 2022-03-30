import os
import pytz
import logging
from time import time
from datetime import datetime
from pyrogram import Client, filters, idle
from config import BOT, LOGS, BOT_USERNAME, DUMP_GRP, SPY_GRP
from logging import INFO, FileHandler, StreamHandler, basicConfig, getLogger

# Logging 
basicConfig(
    format="> %(asctime)s | %(name)s [%(levelname)s] <> %(message)s",
    level=INFO,
    datefmt="%d/%m/%Y, %H:%M:%S",
    handlers=[FileHandler("PHDLBot.log"), StreamHandler()],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.dispatcher").setLevel(logging.INFO)
LOGS.info("Starting Deployment...")

BOT.start()
try:
    BOT.send_message(chat_id=SPY_GRP, text="Bot Started!")
except:
    LOGS.info("Kindly make a Public Group/Channel and put it's Username in SPY_GRP rather than Channel ID of a Pvt Channel/Group")
idle()

BOT.stop()
LOGS.info("Bot Stopped!")
