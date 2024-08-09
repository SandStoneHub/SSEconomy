import logging
import config
from datetime import datetime

current_datetime = datetime.now()

# logging.basicConfig(level=logging.INFO, filename=f"log/{current_datetime.year}_{current_datetime.month}_{current_datetime.day}_{current_datetime.hour}_{current_datetime.minute}_{current_datetime.second}.log",filemode="w")

def log(msg):
    logging.info(msg)

async def discord_log(bot, msg):
    channel = bot.get_channel(config.log_channel)
    await channel.send(msg)