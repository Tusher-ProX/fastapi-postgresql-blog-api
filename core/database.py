# import os 
# from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base
from core.config import settings

# load_dotenv() # instead of this we use config file as settings to load .env file

# POSTGRES_DATABASE_URL = os.environ.get("DATABASE_URL") 

POSTGRES_DATABASE_URL = settings.database_url

if not POSTGRES_DATABASE_URL:
    raise ValueError("Error: Can Not Find .env files Database URL")
else: 
    print("Database connected Successfully")

engine = create_engine( 
    POSTGRES_DATABASE_URL
)

sessionLocal = sessionmaker(
    bind= engine,
    autoflush= False,
    autocommit= False
)

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=convention)

def get_db():
    db = sessionLocal()

    try:
        yield db

    finally:
        db.close()