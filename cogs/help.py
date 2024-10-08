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
За каждое сообщения вы будите получать от 1 до 2 **Камушек**, а за каждую минуту в голосовом канале получать от 1 до 3 **Камушек**

**УЧТИТЕ!**, что за спам, афк в воисе, использования твинков ваш аккаунт в боте будет Заблокирован!

**Команды**
`/profile` — Профиль в боте
`/pay` — Перевести камушки
`/shop` — Магазин ролей
`/admin` — Админ панель

*Текущая версия бота: **{config.ver}** *
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
За каждое сообщения вы будите получать 1 до 2 **Камушек**, а за каждую минуту в голосовом канале получать от 1 до 3 **Камушкек**

**УЧТИТЕ!**, что за спам, афк в воисе, использования твинков ваш аккаунт в боте будет Заблокирован!

**Команды**
`/profile` — Профиль в боте
`/pay` — Перевести камушки
`/shop` — Магазин ролей

*Текущая версия бота: **{config.ver}**  *
                """,
                color=config.embed_color  
            )
            await ctx.send(embed=embed)
            
def setup(bot):
    bot.add_cog(Help(bot))