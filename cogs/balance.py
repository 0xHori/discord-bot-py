import os
import sqlite3

import disnake
from disnake.ext import commands


class BalanceCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def balance(self, inter: disnake.GuildCommandInteraction, member: disnake.Member = None):
        """Получение баланса"""
        print(os.getcwd())
        connection = sqlite3.connect('./data/database.db')
        cursor = connection.cursor()

        user = member or inter.author
        user_id = user.id
        if (cursor.execute('SELECT * FROM data WHERE id = ?', (user_id,))).fetchone() is None:
            cursor.execute('INSERT INTO data(id, coin_hand, coin_bank, diamond) VALUES (?, ?, ?, ?)', (user_id, 0, 0, 0))
            connection.commit()
        res = cursor.execute('SELECT coin_hand, coin_bank, diamond FROM data WHERE id = ?', (user_id,))
        user_coin_hand, user_coin_bank, user_diamond, = res.fetchone()


        connection.close()
        embed = disnake.Embed(title=f"Баланс {user}")
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="> Монеты", value=f"```{user_coin_hand + user_coin_bank}```")
        embed.add_field(name="> Алмазы", value=f"```{user_diamond}```")
        await inter.response.send_message(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(BalanceCommand(bot))