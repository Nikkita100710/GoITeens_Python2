from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from databases import Database

DATABASE_URL = 'sqlite:///test.db'
DATABASE = create_engine('sqlite:///test.db')
metadata = MetaData()
database = Database(DATABASE_URL)
app = FastAPI()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer)
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get('/users/{user_id}')
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    return {'user': user}
