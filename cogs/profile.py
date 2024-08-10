import disnake
import config
from disnake.ext import commands
from database.sql import select_from_db

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="profile", description="Профиль на сервере")
    async def profile(self, ctx, member: disnake.Member = commands.Param(description="Выбери, чей профиль хочешь посмотреть", default=None)):
        
        user = ctx.author
        user_id = user.id
        balance = select_from_db(user_id, "count")

        status = select_from_db(user_id, "status")
        if status == "ban":
            reason = select_from_db(user_id, "reason")
            await ctx.send(f"⛔ Ваш аккаунт заблокирован! Для разблокировки обратитесь в поддержку\nПричина: ||{reason}||", ephemeral=True)
            return

        if member is not None:
            user = member
            user_id = user.id
            status = select_from_db(user_id, "status")
            balance = select_from_db(user_id, "count")

            if member.bot == True:
                await ctx.send("Нельзя смотреть профиль ботов!", ephemeral=True)
                return
            
            if status == "ban":
                await ctx.send("⛔ Данный пользователь заблокирован и до разблокировки его профиль смотреть нельзя", ephemeral=True)
                return

        name = user.display_name
        username = user.name

        embed = disnake.Embed(
            title=f"Профиль **{name}**",
            description=f"""
            Никнейм: `{username}`

            id: ||**{user_id}**||

            Баланс: **{balance}** Камушек
            """,
            color=config.embed_color  
        )
        embed.set_thumbnail(url=user.avatar.url)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Profile(bot))