import sqlite3

import disnake
from disnake.ext import commands

from utils.data import user_on_db_check


class WithdrawCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def withdraw(self, inter: disnake.GuildCommandInteraction, amount: commands.Range[int, 25, None]):
        """
        Снять деньги со счёта

        Parameters
        ----------
        amount: :class:`int`
            Сумма снятия (от 25)
        """

        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()

        """Если пользователя нет в базе данных, то мы его добавляем в неё."""
        await user_on_db_check(connection, cursor, inter.author.id)

        res = cursor.execute('SELECT coin_hand, coin_bank FROM data WHERE id = ?', (inter.author.id,))
        author_coin_hand, author_coin_bank = res.fetchone() # 1 на руках балик, 2 в банке балик

        if author_coin_bank < amount:
            embed = disnake.Embed(title=f"{inter.author.name}, брат у тебя столько денег нет, у тебя {author_coin_bank} на счету")
            await inter.response.send_message(embed=embed)
        elif author_coin_bank >= amount:
            cursor.execute('UPDATE data SET coin_bank = ? WHERE id = ?', (author_coin_bank - amount, inter.author.id))
            connection.commit()
            cursor.execute('UPDATE data SET coin_hand = ? WHERE id = ?', (author_coin_hand + amount, inter.author.id))
            connection.commit()
            embed = disnake.Embed(title=f"{inter.author.name}, ты снял со счёта {amount} валюты")
            await inter.response.send_message(embed=embed)

        connection.close()



def setup(bot: commands.Bot):
    bot.add_cog(WithdrawCommand(bot))