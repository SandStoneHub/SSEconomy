import disnake
import config
from disnake.ext import commands
from database.sql import select_all_from_db, select_from_db, update_in_db
from logs.logger import discord_log

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="shop", description="Открыть магазин сервера")
    async def shop(self, ctx): 

        user_id = ctx.author.id

        status = select_from_db(user_id, "status")
        if status == "ban":
            reason = select_from_db(user_id, "reason")
            await ctx.send(f"⛔ Ваш аккаунт заблокирован! Для разблокировки обратитесь в поддержку\nПричина: ||{reason}||", ephemeral=True)
            return

        embed = disnake.Embed(
            title=f"Магазин ролей",
            color=config.embed_color  
        )

        components = []
        roles = select_all_from_db("roles")
        roles.sort(key=lambda role: role[1])

        for role in roles:
            button = disnake.ui.Button(label=role[2], style=disnake.ButtonStyle.success, custom_id=str(role[0]))
            embed.add_field(name=f"{role[2]}", value=f"Цена: **{role[1]}** камушков", inline=False)

            components.append(button)

        await ctx.send(embed=embed, components=components)
        components = []

    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.AppCmdInter):

        roles = select_all_from_db("roles")
        roles.sort(key=lambda role: role[1])

        if interaction.component.custom_id in [str(role[0]) for role in roles]:
            role = [role for role in roles if role[0] == int(interaction.component.custom_id)][0]
            guild = interaction.guild
            user = interaction.author
            user_id = user.id
            role_to_add = guild.get_role(role[0])

            if role_to_add in user.roles:
                await interaction.response.send_message(f"{user.mention} Вы уже преобрели роль **{role[2]}**!", ephemeral=True)
                await discord_log(self.bot, f"{user.mention} Пытался преобрести роль **{role[2]}**")
                return
            
            balance = int(select_from_db(user_id, "count"))
            role_price = int(role[1])

            if balance < role_price:
                await interaction.response.send_message(f"{user.mention} Недостаточно средст", ephemeral=True)
                await discord_log(self.bot, f"{user.mention} Пытался преобрести роль **{role[2]}**")
                return

            update_in_db(user_id, "count", balance-role_price)
            
            await user.add_roles(role_to_add)
            await interaction.response.send_message(f"{user.mention} Успешно преобрел роль **{role[2]}**!")
            await discord_log(self.bot, f"{user.mention} Преобрел роль **{role[2]}**")
            
def setup(bot):
    bot.add_cog(Shop(bot))