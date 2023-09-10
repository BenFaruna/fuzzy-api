import os

from flask import Flask

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_app():
    app = Flask(__name__)
    return app

def create_database_session():
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    print(DB_URL)

    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session
