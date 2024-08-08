import disnake
from disnake.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="admin", description="Админ панель")
    @commands.has_guild_permissions(administrator=True)
    async def admin(self, ctx): 
        pass
            
def setup(bot):
    bot.add_cog(Admin(bot))