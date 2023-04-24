import models
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

USERNAME = "domingol"
DATABASE_NAME = 'EPICDATABASE'
engine = create_engine(f"postgresql+psycopg2://{USERNAME}:@localhost:5431/{DATABASE_NAME}")
if not database_exists(engine.url):
    create_database(engine.url)

print(database_exists(engine.url))

models.Base.metadata.create_all(engine)