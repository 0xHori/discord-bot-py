import disnake
from disnake.ext import commands


class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def help(self, inter: disnake.GuildCommandInteraction):
        """Список команд"""
        embed = disnake.Embed(title="📋 Справка по командам бота", description="Привет! Привет! Я — экономический бот этого сервера. Вот что я умею:")
        embed.add_field(name="💰 Экономика", value="> `/balance` — Посмотреть свой баланс.\n\
                                                    > `/pay` — Передать валюту другому участнику", inline=False)
        embed.add_field(name="🖼️ Прочее", value="> `/avatar` — Получить аватар участника.\n\
                                                 > `/guild` — Информация о сервере", inline=False)
        embed.set_footer(text="Если вы хотите предложить улучшение, свяжитесь с создателем!")
        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(HelpCommand(bot))