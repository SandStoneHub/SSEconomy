import disnake
from disnake.ext import commands
from database.sql import select_from_db, update_in_db
from logs.logger import log, discord_log

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="pay", description="Перевести камушки")
    async def pay(self, ctx, member: disnake.User, amount: int): 

        if member.bot == True:
            await ctx.send("Ботам нельзя переводит короны!", ephemeral=True)
            return
        
        user = ctx.author
        user_id = user.id
        member_id = member.id
        balance = select_from_db(user_id, "count")
        member_balance = select_from_db(member_id, "count")

        if balance < amount:
            await ctx.send("Недостаточно средств для перевода", ephemeral=True)
            await discord_log(self.bot, f"{user.mention} Пытался перевести **{amount}** Камушков {member.mention}")
            return
        
        if amount < 100:
            await ctx.send("Минимальная сумма перевода **100** камушков!", ephemeral=True)
            await discord_log(self.bot, f"{user.mention} Пытался перевести **{amount}** Камушков {member.mention}")
            return

        update_in_db(user_id, "count", balance-amount)
        update_in_db(member_id, "count", member_balance+amount)
        await ctx.send(f"{user.mention} Вы успешно перевели {member.mention} **{amount}** Камушков!")

        await discord_log(self.bot, f"{user.mention} Перевел **{amount}** Камушков {member.mention}")
            
def setup(bot):
    bot.add_cog(Pay(bot))