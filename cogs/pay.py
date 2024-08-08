import disnake
from disnake.ext import commands

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="pay", description="Перевести деньги")
    async def pay(self, ctx): 
        pass
            
def setup(bot):
    bot.add_cog(Pay(bot))