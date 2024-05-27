from databases import Database

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)


async def connect_db():
    await database.connect()


async def disconnect_db():
    await database.disconnect()

