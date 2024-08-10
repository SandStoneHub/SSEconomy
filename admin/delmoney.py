import disnake
import config
from disnake import TextInputStyle
from database.sql import update_in_db, select_from_db
from logs.logger import discord_log

class DelMoney(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot

        components = [
            disnake.ui.TextInput(
                label="ID",
                placeholder="Введите id пользователя",
                custom_id="user_id",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Вычесть с баланса",
                placeholder="Введите кол-во чтобы вычесть с баланса",
                custom_id="count",
                style=TextInputStyle.short,
                max_length=7,
            ),
        ]
        super().__init__(title="Вычесть с баланса", components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        user_id = ""
        money = ""

        embed = disnake.Embed(
            title="Вычтено с баланса",
            color=config.embed_color
        )

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

            if key.capitalize() == "User_id": user_id = int(value[:1024])
            if key.capitalize() == "Count": money = int(value[:1024])
        
        guild = inter.guild
        members = await guild.fetch_members(limit=None).flatten()
        user_ids = []
        
        for member in members:
            user_ids.append(member.id)

        if user_id in user_ids: pass
        else:
            await inter.response.send_message("Аккаунт с таким id не найден!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался вычисть с баланса **{money}** не существуешему аккаунту (id: {user_id})")
            return
        
        users = guild.get_member(user_id)
        if users.bot:
            await inter.response.send_message("Ботам нельзя вычитать баланс!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался вычисть баланс боту <@{user_id}> на **{money}**")
            return

        balance = int(select_from_db(user_id, "count"))

        if money <= 0:
            await inter.response.send_message("Для поплнения баланса нажмите на кнопку **Пополнить баланс**!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался вычисть баланс <@{user_id}> на **{money}**")
            return
        
        if balance < money:
            await inter.response.send_message("Нельзя сделать баланс отрицательным!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался вычисть баланс <@{user_id}> на **{money}**")
            return

        update_in_db(user_id, "count", balance-money)

        await inter.response.send_message(embed=embed, ephemeral=True)
        await discord_log(self.bot, f"{inter.author.mention} Вычил баланс <@{user_id}> на **{money}**")