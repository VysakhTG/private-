import os
import redis
import asyncio
from pyrogram import filters
from config import REDIS_URI, REDIS_PWD, OWNER, LOGS, BOT, DUMP_GRP, BOT_USERNAME

# Redis ans DB Stuffs
def connect_redis():
   redis_info = REDIS_URI.split(":")
   LOGS.info("Trying to Establish Connection with DATABASE")
   return redis.Redis(
            host=redis_info[0],
            port=redis_info[1],
            password=REDIS_PWD,
            decode_responses=True,
        )

def redis_connection():
   My_DB = connect_redis()
   try:
      My_DB.ping()
      LOGS.info("Connection with DataBase successfully established")
   except BaseException:
      LOGS.info("Can't connect to DataBase")
   return My_DB

DB = redis_connection()

# Checking the DataBase
try:
   sudos = DB["SUDOS"]
   LOGS.info(f"SUDO-USERS = {sudos}")
except Exception as e:
   DB["SUDOS"] = OWNER
   LOGS.info("No Sudo User was Found. Setting up the Database for the First Time...")
   LOGS.info("")
   
try:
   users = DB["USERS"]
   number = len(users.split(" "))  
   LOGS.info(f"{number} Users are Currently using this bot.")
except Exception as e:
   DB["USERS"] = OWNER
   LOGS.info("Setting Up the BOT for first time use")
   
vids = len(DB.keys())
LOGS.info(f"TOTAL VIDEOS IN DATABASE - {vids}")

# SUDO USERS
SUDOERS = set(int(x) for x in DB["SUDOS"].split())
sudo_filter = filters.create(
    lambda _, __, msg:
    (msg.from_user and msg.from_user.id in SUDOERS) or msg.outgoing or (msg.from_user and msg.from_user.id == int(OWNER))
)
