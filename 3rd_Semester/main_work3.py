import uvicorn
from fastapi import FastAPI, Query, Path
import sqlite3
from databases import Database
from sqlalchemy import create_engine, Column, String, Integer, MetaData, Table
import asyncio


DATABASE_URL = 'sqlite:///test.db'
DATABASE = create_engine('sqlite:///test.db')
metadata = MetaData()
database = Database(DATABASE_URL)
app = FastAPI()


cars = Table('cars',
             metadata,
             Column('id', Integer, primary_key=True),
             Column('model', String)
 )

metadata.create_all(DATABASE)

@app.on_event('startup')
async def startup():
    await database.connect()



@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()



@app.get('/cars/{car_id}')
async def read_car(car_id: int = Path(..., title="Id of car", description="This is the id of a current car"), text: str = Query("", title="", description="") ):
    query = cars.select().where(cars.c.id == car_id)
    car = await database.fetch_one(query)
    return {'car': car}


if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)

