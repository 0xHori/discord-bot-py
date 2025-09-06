import disnake
from disnake.ext import commands


class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def balance(self, inter: disnake.GuildCommandInteraction):
        """Получение баланса"""
        embed = disnake.Embed(title=f"Баланс {inter.user.name}", )
        embed.set_thumbnail(url=inter.user.display_avatar.url)
        embed.add_field(name="> Монеты", value="```{balance}```")
        embed.add_field(name="> Алмазы", value="```{balance}```")
        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(BalanceCommand(bot))