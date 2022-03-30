import os
from dotenv import load_dotenv
from logging import getLogger
from pyrogram import Client, idle 

# Environment Variables and Client
if os.path.exists(".env"):
    load_dotenv(".env")

API_ID = int(os.getenv("API_ID", "6"))
API_HASH = os.getenv("API_HASH", "eb06d4abfb49dc3eeb1aeb98ae0f581e")
BOT_TOKEN = os.getenv("BOT_TOKEN")
REDIS_URI = os.getenv("REDIS_URI")
REDIS_PWD = os.getenv("REDIS_PWD")
OWNER = int(os.getenv("OWNER"))
BOT_USERNAME = os.getenv("BOT_USERNAME", "PHDL_RoBot")
DUMP_GRP = os.getenv("DUMP_GRP")
SPY_GRP = os.getenv("SPY_GRP")

LOGS = getLogger("pornbot")
BOT = Client("pornbot", API_ID, API_HASH, bot_token=BOT_TOKEN, plugins=dict(root="PHB"))
