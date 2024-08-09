import disnake
import config
from disnake import TextInputStyle
from database.sql import update_in_db, select_from_db
from logs.logger import discord_log

class Unban(disnake.ui.Modal):
    def __init__(self, bot):
        self.bot = bot

        components = [
            disnake.ui.TextInput(
                label="ID",
                placeholder="Введите id пользователя",
                custom_id="user_id",
                style=TextInputStyle.short,
                max_length=50,
            )
        ]
        super().__init__(title="Забанить пользователя", components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        user_id = ""

        embed = disnake.Embed(
            title="Забанен пользователь",
            color=config.embed_color
        )

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

            if key.capitalize() == "User_id": user_id = int(value[:1024])

        guild = inter.guild
        members = await guild.fetch_members(limit=None).flatten()
        user_ids = []
        
        for member in members:
            user_ids.append(member.id)

        if user_id in user_ids: pass
        else:
            await inter.response.send_message("Аккаунт с таким id не найден!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался разблокировать не существующий аккаунту (id: {user_id})")
            return
        
        users = guild.get_member(user_id)
        if users.bot:
            await inter.response.send_message("Ботов нельзя блокировать!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался разблокировать аккаунт боту <@{user_id}>")
            return
        
        status = select_from_db(user_id, "status")
        if status == "user":
            await inter.response.send_message("Пользователь не заблокирован!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался разблокировать не заблокированного пользователя <@{user_id}>")
            return
        
        update_in_db(user_id, "status", "user")

        await inter.response.send_message(embed=embed, ephemeral=True)
        await discord_log(self.bot, f"{inter.author.mention} Разблокировал аккаунт <@{user_id}>")