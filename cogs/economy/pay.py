import sqlite3

import disnake
from disnake.ext import commands


class PayCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def pay(self, inter: disnake.GuildCommandInteraction, member: disnake.Member, amount: commands.Range[int, 25, None]):
        """
        Передать валюту другому пользователю

        Parameters
        ----------
        member: :class:`disnake.Member`
            Какому пользователю перевести
        amount: :class:`int`
            Сумма перевода (от 25)
        """

        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()
        """Если пользователя нет в базе данных, то мы его добавляем в неё."""
        if (cursor.execute('SELECT * FROM data WHERE id = ?', (inter.author.id,))).fetchone() is None:
            cursor.execute('INSERT INTO data(id, coin_hand, coin_bank, diamond) VALUES (?, ?, ?, ?)',
                           (inter.user.id, 0, 0, 0,))
            connection.commit()
        if (cursor.execute('SELECT * FROM data WHERE id = ?', (member.id,))).fetchone() is None:
            cursor.execute('INSERT INTO data(id, coin_hand, coin_bank, diamond) VALUES (?, ?, ?, ?)',
                           (member.id, 0, 0, 0,))
            connection.commit()


        author_res = cursor.execute('SELECT coin_bank FROM data WHERE id = ?', (inter.author.id,))
        author_coin_bank, = author_res.fetchone()

        member_res = cursor.execute('SELECT coin_bank FROM data WHERE id = ?', (member.id,))
        member_coin_bank, = member_res.fetchone()

        if author_coin_bank < amount:
            embed = disnake.Embed(
                title=f"{inter.author.name}, брат у тебя столько денег нет, у тебя {author_coin_bank} на счету")
            await inter.response.send_message(embed=embed)
        elif author_coin_bank >= amount:
            # меняем балик в банке отправителя средств
            cursor.execute('UPDATE data SET coin_bank = ? WHERE id = ?', (author_coin_bank - amount, inter.author.id))
            connection.commit()
            # меняем балик в банке получателя средств
            cursor.execute('UPDATE data SET coin_bank = ? WHERE id = ?', (member_coin_bank + amount, member.id))
            connection.commit()
            embed = disnake.Embed(title=f"{inter.author.name}, ты перевёл со своего банковского счёта {amount} валюты на банковский счёт {member.name}")
            await inter.response.send_message(embed=embed)



def setup(bot: commands.Bot):
    bot.add_cog(PayCommand(bot))