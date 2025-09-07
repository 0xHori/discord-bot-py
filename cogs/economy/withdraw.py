import sqlite3

import disnake
from disnake.ext import commands


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
        if (cursor.execute('SELECT * FROM data WHERE id = ?', (inter.user.id,))).fetchone() is None:
            cursor.execute('INSERT INTO data(id, coin_hand, coin_bank, diamond) VALUES (?, ?, ?, ?)', (inter.user.id, 0, 0, 0))
            connection.commit()
            embed = disnake.Embed(title=f"{inter.user.name}, тебя в базе нет, я тебя добавил. какой витхдров блин")
            await inter.response.send_message(embed=embed)
        else:
            res = cursor.execute('SELECT coin_hand, coin_bank FROM data WHERE id = ?', (inter.user.id,))
            user_coin_hand, user_coin_bank = res.fetchone() # 1 на  балик, 2 в банке балик
            if user_coin_bank < amount:
                embed = disnake.Embed(title=f"{inter.user.name}, брат у тебя столько денег нет, у тебя {user_coin_bank} на счету")
                await inter.response.send_message(embed=embed)
            elif user_coin_bank >= amount:
                # меняем балик в банке
                cursor.execute('UPDATE data SET coin_bank = ? WHERE id = ?', (user_coin_bank - amount, inter.user.id))
                connection.commit()
                # меняем балик на руках
                cursor.execute('UPDATE data SET coin_hand = ? WHERE id = ?', (user_coin_hand + amount, inter.user.id))
                connection.commit()
                embed = disnake.Embed(title=f"{inter.user.name}, ты снял со счёта {amount} валюты")
                await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(WithdrawCommand(bot))