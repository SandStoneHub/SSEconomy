import disnake
from disnake.ext import commands
from database.sql import select_from_db, update_in_db
from logs.logger import log, discord_log

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="pay", description="Перевести камушки")
    async def pay(self, ctx, member: disnake.User, amount: int): 

        user = ctx.author
        user_id = user.id
        member_id = member.id
        balance = select_from_db(user_id, "count")
        member_balance = select_from_db(member_id, "count")
        status = select_from_db(user_id, "status")

        if status == "ban":
            reason = select_from_db(user_id, "reason")
            await ctx.send(f"⛔ Ваш аккаунт заблокирован! Для разблокировки обратитесь в поддержку\nПричина: ||{reason}||", ephemeral=True)
            await discord_log(self.bot, f"{user.mention} Пытался перевести **{amount}** на баланс {member.mention}")
            return

        if member.bot == True:
            await ctx.send("Ботам нельзя переводит короны!", ephemeral=True)
            await discord_log(self.bot, f"{user.mention} Пытался перевести **{amount}** на баланс бота {member.mention}")
            return

        if balance < amount:
            await ctx.send("Недостаточно средств для перевода", ephemeral=True)
            await discord_log(self.bot, f"{user.mention} Пытался перевести **{amount}** на баланс {member.mention}")
            return
        
        if amount < 100:
            await ctx.send("Минимальная сумма перевода **100** камушков!", ephemeral=True)
            await discord_log(self.bot, f"{user.mention} Пытался перевести **{amount}** на баланс {member.mention}")
            return

        update_in_db(user_id, "count", balance-amount)
        update_in_db(member_id, "count", member_balance+amount)

        await ctx.send(f"{user.mention} Вы успешно перевели {member.mention} **{amount}** Камушков!")

        user = ctx.guild.get_member(member_id)
        await user.send(f"<@{user_id}> Перевел вам на баланс **{amount}** Камушков!")

        await discord_log(self.bot, f"<@{user_id}> Перевел **{amount}** на баланс {member.mention}")
            
def setup(bot):
    bot.add_cog(Pay(bot))