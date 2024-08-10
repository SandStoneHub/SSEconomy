import disnake
import config
from disnake import TextInputStyle
from database.sql import update_in_db, select_from_db
from logs.logger import discord_log

class Ban(disnake.ui.Modal):
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
                label="Причина",
                placeholder="Укажите причину блокировки",
                custom_id="reason",
                style=TextInputStyle.short,
                max_length=100,
            ),
        ]
        super().__init__(title="Заблокировать пользователя", components=components)

    async def callback(self, inter: disnake.ModalInteraction):

        user_id = ""
        reason = ""

        embed = disnake.Embed(
            title="Заблокирован пользователь",
            color=config.embed_color
        )

        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )

            if key.capitalize() == "User_id": user_id = int(value[:1024])
            if key.capitalize() == "Reason": reason = value[:1024]

        guild = inter.guild
        members = await guild.fetch_members(limit=None).flatten()
        user_ids = []
        
        for member in members:
            user_ids.append(member.id)

        if user_id in user_ids: pass
        else:
            await inter.response.send_message("Аккаунт с таким id не найден!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался заблокировать не существующий аккаунту (id: {user_id}) \nПричина: ||{reason}||")
            return
        
        users = guild.get_member(user_id)
        if users.bot:
            await inter.response.send_message("Ботов нельзя блокировать!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался заблокировать аккаунт боту <@{user_id}> \nПричина: ||{reason}||")
            return
        
        status = select_from_db(user_id, "status")
        if status == "ban":
            await inter.response.send_message("Пользователь уже заблокирован!", ephemeral=True)
            await discord_log(self.bot, f"{inter.author.mention} Пытался заблокировать уже заблокированного пользователя <@{user_id}> \nПричина: ||{reason}||")
            return
        
        update_in_db(user_id, "status", "ban")
        update_in_db(user_id, "reason", reason)

        await inter.response.send_message(embed=embed, ephemeral=True)

        user = guild.get_member(user_id)
        await user.send(f"⛔ Ваш аккаунт заблокирован! Для разблокировки обратитесь в поддержку\nПричина: ||{reason}||")

        await discord_log(self.bot, f"{inter.author.mention} Заблокировал аккаунт <@{user_id}> \nПричина: ||{reason}||")