import os
from dotenv import load_dotenv
import disnake
from disnake.ext import commands

load_dotenv()

TOKEN: str = os.environ["TOKEN"]

bot = commands.InteractionBot(test_guilds=[1385772851587715092], sync_commands_debug=True)

@bot.event
async def on_ready():
    print("The bot is ready!")


bot.load_extension("cogs.ping")


bot.run(TOKEN)


