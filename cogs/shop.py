import disnake
from disnake.ext import commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="shop", description="Открыть магазин сервера")
    async def shop(self, ctx): 
        pass
            
def setup(bot):
    bot.add_cog(Shop(bot))