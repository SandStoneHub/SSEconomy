import asyncio
import random
from database.sql import update_in_db, select_from_db
from config import afk_voice

async def add_count_to_user(bot):
    while True:
        for guild in bot.guilds:
            for member in guild.members:
                if member.voice:
                    user_id = member.id
                    status = select_from_db(user_id, "status")
                    
                    if member.voice and member.voice.channel and member.voice.channel.id == afk_voice: continue
                    if member.bot: continue
                    if status == "ban": continue
                        
                    balance = select_from_db(user_id, "count")
                    count = random.randint(1, 3)
                    update_in_db(user_id, "count", balance+count)
                
        await asyncio.sleep(30)