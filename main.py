import disnake 
from disnake.ext import commands
from disnake import Activity, ActivityType
import os
import config
import platform
import random
from database.sql import select_from_db, add_to_db, update_in_db
from voice_farm import add_count_to_user

intents = disnake.Intents.default()
intents.presences = True
intents.members = True

TOKEN = config.TOKEN

bot = commands.Bot(command_prefix=None, intents=intents, reload=True)

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

for filename in os.listdir(config.cogs_path):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

@bot.event
async def on_ready():
    print(f"Бот {bot.user} успешно запущен в версии {config.ver}")
    await bot.change_presence(status=disnake.Status.online,activity=Activity(name="за экономикой",  type=ActivityType.watching))

@bot.event
async def on_member_join(member):
    if member.bot: return
    add_to_db(member.id)

@bot.listen("on_message")
async def on_message(message):
    user = message.author
    user_id = user.id

    if user.bot: return

    if message.channel.id in config.msg_channl:
        balance = select_from_db(user_id, "count")
        count = random.randint(1, 3)
        update_in_db(user_id, "count", balance+count)

# if platform.system() != "Windows": TOKEN = config.TOKEN
bot.loop.create_task(add_count_to_user(bot))
bot.run(TOKEN)