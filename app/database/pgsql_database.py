from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config.config import Config

SQLALCHEMY_DATABASE_URL = f'postgresql://postgres:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:5432/{Config.POSTGRES_DB}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
