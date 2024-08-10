import disnake
import config
import random
from disnake.ext import commands
from database.sql import select_from_db, update_in_db

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        user_id = user.id

        status = select_from_db(user_id, "status")

        if status == "ban" or user.bot: return

        if message.channel.id in config.msg_channl:
            balance = select_from_db(user_id, "count")
            count = random.randint(1, 3)
            update_in_db(user_id, "count", balance+count)
            
def setup(bot):
    bot.add_cog(OnMessage(bot))