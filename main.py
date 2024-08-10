import disnake 
from disnake.ext import commands
from disnake import Activity, ActivityType
import os
import config
import platform
from database.sql import add_to_db
from voice_farm import add_count_to_user

intents = disnake.Intents.default()
intents.presences = True
intents.members = True

TOKEN = config.TOKEN
cogs_path = config.cogs_path

bot = commands.Bot(command_prefix=None, intents=intents, reload=True)

if platform.system() != "Windows": cogs_path = config.cogs_path_ubu

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

for filename in os.listdir(cogs_path):
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

bot.loop.create_task(add_count_to_user(bot))
bot.run(TOKEN)