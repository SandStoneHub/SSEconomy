import disnake
import config
from disnake.ext import commands
from logs.logger import discord_log
from admin.addmoney import AddMoney
from admin.delmoney import DelMoney
from admin.ban import Ban
from admin.unban import Unban

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="admin", description="Админ панель")
    async def admin(self, ctx):

        if ctx.author.guild_permissions.administrator == False:
            await ctx.send("Не удалось открыть панель", ephemeral=True)
            await discord_log(self.bot, f"{ctx.author.mention} Пытался открыть админ панель")
            return

        components=[
            [
                disnake.ui.Button(label="Пополнить Баланс", style=disnake.ButtonStyle.success, custom_id="add_money"),
                disnake.ui.Button(label="Вычесть с баланса", style=disnake.ButtonStyle.success, custom_id="del_money")
            ],

            [
                disnake.ui.Button(label="Заблокировать", style=disnake.ButtonStyle.danger, custom_id="ban"),
                disnake.ui.Button(label="Разблокировать", style=disnake.ButtonStyle.danger, custom_id="unban")
            ]
        ]

        embed = disnake.Embed(
            title=f"Админ Панель",
            color=config.embed_color  
        )

        await ctx.send(embed=embed, components=components, ephemeral=True)

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.AppCmdInter):
        if inter.component.custom_id == "add_money":
            await inter.response.send_modal(modal=AddMoney(self.bot))
        if inter.component.custom_id == "del_money":
            await inter.response.send_modal(modal=DelMoney(self.bot))
        if inter.component.custom_id == "ban":
            await inter.response.send_modal(modal=Ban(self.bot))
        if inter.component.custom_id == "unban":
            await inter.response.send_modal(modal=Unban(self.bot))


def setup(bot):
    bot.add_cog(Admin(bot))