import disnake
import config
from disnake.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="help", description="Информация о боте")
    async def help(self, ctx): 
        if ctx.author.guild_permissions.administrator:
            embed = disnake.Embed(
                title=f"SSEconomy",
                description=f"""
**Информация**
Бот-экономика для официального дискорд сервера **SandStone**
Волюта сервер — **Камушки**
Для их получения проявляйте активность
За каждое сообщения и минуту в голосовом канале вы будите получать от 1 до 3 **Камушков**

**УЧТИТЕ!**, что за спам, афк в воисе, использования твинков ваш аккаунт в боте будет Заблокирован!

**Команды**
`/profile` — Профиль в боте
`/pay` — Перевести камушки
`/shop` — Магазин ролей
`/admin` — Админ панель
                """,
                color=config.embed_color  
            )
            await ctx.send(embed=embed)
        else:
            embed = disnake.Embed(
                title=f"SSEconomy",
                description=f"""
**Информация**
Бот-экономика для официального дискорд сервера **SandStone**
Волюта сервер — **Камушки**
Для их получения проявляйте активность
За каждое сообщения и минуту в голосовом канале вы будите получать от 1 до 3 **Камушков**

**УЧТИТЕ!**, что за спам, афк в воисе, использования твинков ваш аккаунт в боте будет Заблокирован!

**Команды**
`/profile` — Профиль в боте
`/pay` — Перевести камушки
`/shop` — Магазин ролей
                """,
                color=config.embed_color  
            )
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Help(bot))