import disnake
from disnake.ext import commands


class GuildCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def guild(self, inter: disnake.GuildCommandInteraction):
        """Получение информации о сервере"""
        embed = disnake.Embed(title=f"ℹ Информация о сервере {inter.guild.name}")
        embed.add_field(name="🆔 ID сервера", value=f"{inter.guild.id}", inline=False)
        embed.add_field(name="👑 Владелец", value=f"<@{inter.guild.owner_id}>\n`{inter.guild.owner_id}`", inline=False)
        embed.add_field(name="📆 Дата создания", value=f"`{inter.guild.created_at}`", inline=False)
        embed.add_field(name="👥 Участники", value=f"Всего: `{inter.guild.member_count}`", inline=False)
        embed.add_field(name="🎭 Роли", value=f"Всего: `{0}`", inline=False)
        embed.add_field(name="📚 Каналы", value=f"💬 Текстовые: `{0}`\n🎙️ Голосовые: `{0}`\n📁 Всего: `{0}`", inline=False)
        embed.add_field(name="🛡️ Уровень проверки", value=f"`{inter.guild.verification_level}`", inline=False)
        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(GuildCommand(bot))