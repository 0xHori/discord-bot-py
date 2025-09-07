import disnake
from disnake.ext import commands


class AvatarCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def avatar(self, inter: disnake.GuildCommandInteraction, member: disnake.Member = None):
        """
        Получить аватар участника

        Parameters
        ----------
        member: :class:`disnake.Member`
            Чей аватар хочешь получить

        """

        member = member or inter.author
        embed = disnake.Embed(title=f"Аватар {member.name}")
        embed.set_image(url=member.display_avatar.url)
        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(AvatarCommand(bot))