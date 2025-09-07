import sqlite3

import disnake
from disnake.ext import commands


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

        if (cursor.execute('SELECT * FROM data WHERE id = ?', (inter.user.id,))).fetchone() is None:
            cursor.execute('INSERT INTO data(id, coin_hand, coin_bank, diamond) VALUES (?, ?, ?, ?)', (inter.user.id, 0, 0, 0))
            connection.commit()
            embed = disnake.Embed(title=f"{inter.user.name}, тебя в базе нет, я тебя добавил. какой витхдров блин")
            await inter.response.send_message(embed=embed)
        else:
            res = cursor.execute('SELECT coin_hand, coin_bank FROM data WHERE id = ?', (inter.user.id,))
            user_coin_hand, user_coin_bank = res.fetchone()
            if user_coin_hand < amount:
                embed = disnake.Embed(title=f"{inter.user.name}, брат у тебя столько денег нет, у тебя {user_coin_hand} на руках")
                await inter.response.send_message(embed=embed)
            elif user_coin_hand >= amount:
                # меняем балик на руках
                cursor.execute('UPDATE data SET coin_hand = ? WHERE id = ?', (user_coin_hand - amount, inter.user.id))
                connection.commit()
                # меняем балик в банке
                cursor.execute('UPDATE data SET coin_bank = ? WHERE id = ?', (user_coin_bank + amount, inter.user.id))
                connection.commit()
                embed = disnake.Embed(title=f"{inter.user.name}, ты положил на счёт {amount} валюты")
                await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(DepositCommand(bot))