import os
import sqlite3

import disnake
from disnake.ext import commands

from utils.data import user_on_db_check


class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def balance(self, inter: disnake.GuildCommandInteraction, member: disnake.Member = None):
        """
        Получение баланса

        Parameters
        ----------
        member: :class:`disnake.Member`
            Чей баланс посмотреть
        """
        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()

        user = member or inter.author
        user_id = user.id
        """Если пользователя нет в базе данных, то мы его добавляем в неё."""
        await user_on_db_check(connection, cursor, user_id)

        res = cursor.execute('SELECT coin_hand, coin_bank, diamond FROM data WHERE id = ?', (user_id,))
        user_coin_hand, user_coin_bank, user_diamond, = res.fetchone()

        embed = disnake.Embed(title=f"Баланс {user.name}")
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="> Монеты на руках", value=f"```{user_coin_hand}```")
        embed.add_field(name="> Монеты в банке", value=f"```{user_coin_bank}```")
        embed.add_field(name="> Алмазы", value=f"```{user_diamond}```")
        await inter.response.send_message(embed=embed)

        connection.close()


def setup(bot: commands.Bot):
    bot.add_cog(BalanceCommand(bot))