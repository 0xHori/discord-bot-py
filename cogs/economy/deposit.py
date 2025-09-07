import sqlite3

import disnake
from disnake.ext import commands

from utils.data import user_on_db_check


class DepositCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def deposit(self, inter: disnake.GuildCommandInteraction, amount: commands.Range[int, 25, None]):
        """
        Положить деньги на счёт в банк

        Parameters
        ----------
        amount: :class:`int`
            Сумма пополнения (от 25)
        """

        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()

        """Если пользователя нет в базе данных, то мы его добавляем в неё."""
        await user_on_db_check(connection, cursor, inter.author.id)

        res = cursor.execute('SELECT coin_hand, coin_bank FROM data WHERE id = ?', (inter.author.id,))
        author_coin_hand, author_coin_bank = res.fetchone()

        if author_coin_hand < amount:
            embed = disnake.Embed(title=f"{inter.author.name}, брат у тебя столько денег нет, у тебя {author_coin_hand} на руках")
            await inter.response.send_message(embed=embed)
        elif author_coin_hand >= amount:
            # меняем балик на руках
            cursor.execute('UPDATE data SET coin_hand = ? WHERE id = ?', (author_coin_hand - amount, inter.author.id))
            connection.commit()
            # меняем балик в банке
            cursor.execute('UPDATE data SET coin_bank = ? WHERE id = ?', (author_coin_bank + amount, inter.author.id))
            connection.commit()
            embed = disnake.Embed(title=f"{inter.author.name}, ты положил на счёт {amount} валюты")
            await inter.response.send_message(embed=embed)

        connection.close()


def setup(bot: commands.Bot):
    bot.add_cog(DepositCommand(bot))