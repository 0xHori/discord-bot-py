import os
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()

TOKEN: str = os.environ["TOKEN"]

bot = commands.InteractionBot(test_guilds=[1385772851587715092], sync_commands_debug=True, reload=True)

@bot.event
async def on_ready():
    print("The bot is ready!")


bot.load_extension("cogs.ping")
bot.load_extension("cogs.balance")
bot.load_extension("cogs.guild")


bot.run(TOKEN)


