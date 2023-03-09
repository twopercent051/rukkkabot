import asyncio

import aiomysql

from create_bot import config


async def connection_init():
    host = config.db.host
    user = config.db.user
    password = config.db.password
    db_name = config.db.database
    connection = await aiomysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        db=db_name,
        cursorclass=aiomysql.cursors.DictCursor
    )
    return connection


async def sql_start():
    connection = await connection_init()
    async with connection.cursor() as cursor:
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
            user_id VARCHAR(40),
            username VARCHAR(50),
            name VARCHAR(50),
            message TEXT,
            notification VARCHAR(10),
            sending VARCHAR(10)
            );
            """)
        await cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipients(
            id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, 
            user_id VARCHAR(40),
            rec_id VARCHAR(40),
            rec_username VARCHAR(50),
            rec_name VARCHAR(50) 
            );
            """)
        await cursor.execute("ALTER TABLE messages CONVERT TO CHARACTER SET utf8mb4")
        await cursor.execute("ALTER TABLE recipients CONVERT TO CHARACTER SET utf8mb4")
        print('MySQL connected OK')
        await connection.commit()
        connection.close()


async def get_recipients_sql(user_id):
    connection = await connection_init()
    query = 'SELECT * FROM recipients WHERE user_id = (%s);'
    query_tuple = (user_id,)
    async with connection.cursor() as cursor:
        await cursor.execute(query, query_tuple)
        result = await cursor.fetchall()
    connection.close()
    return result


async def get_message_sql(user_id):
    connection = await connection_init()
    query = 'SELECT * FROM messages WHERE user_id = (%s);'
    query_tuple = (user_id,)
    async with connection.cursor() as cursor:
        await cursor.execute(query, query_tuple)
        result = await cursor.fetchone()
    connection.close()
    return result


async def create_message_sql(user_id, field, value):
    connection = await connection_init()
    query = f'INSERT INTO messages (user_id, {field}) VALUES (%s, %s);'
    query_tuple = (user_id, value)
    async with connection.cursor() as cursor:
        await cursor.execute(query, query_tuple)
    await connection.commit()
    connection.close()


async def update_message_sql(user_id, field, value):
    connection = await connection_init()
    query = f'UPDATE messages SET (user_id, {field}) VALUES (%s, %s);'
    query_tuple = (user_id, value)
    async with connection.cursor() as cursor:
        await cursor.execute(query, query_tuple)
    await connection.commit()
    connection.close()
