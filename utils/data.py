async def user_on_db_check(connection, cursor, user_id):
    if (cursor.execute('SELECT * FROM data WHERE id = ?', (user_id,))).fetchone() is None:
        cursor.execute('INSERT INTO data(id, coin_hand, coin_bank, diamond) VALUES (?, ?, ?, ?)',
                       (user_id, 0, 0, 0,))
        connection.commit()
        return False
    return True