from fastapi import FastAPI, Path, Query
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
from databases import Database

DATABASE_URL = 'sqlite:///test.db'
DATABASE = create_engine(DATABASE_URL)
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
async def read_user(
    user_id: int = Path(..., title="ID of the user", description="This is the ID of the current user"),
    details: str = Query(None, title="Details", description="Additional details to include in the response")
):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    return {'user': user, 'details': details}

