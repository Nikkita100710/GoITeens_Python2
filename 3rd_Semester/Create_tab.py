from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


DATABASE_URL = 'sqlite:///test.db'
engine = create_engine(DATABASE_URL)


metadata = MetaData()


users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('age', Integer)
)


metadata.create_all(engine)
