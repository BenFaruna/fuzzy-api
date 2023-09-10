import os

from typing import Union

from flask import Flask

from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

def create_app() -> Flask:
    app = Flask(__name__)
    return app

def create_database_session() -> Union[Engine, Session]:
    if not os.getenv("DB_URL"):
        DB_NAME = os.getenv("DB_NAME")
        DB_HOST = os.getenv("DB_HOST")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")

        DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    else:
        DB_URL = os.getenv("DB_URL")

    engine = create_engine(DB_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session


def validate_url_parameter(param: str) -> bool:
    """helper function to help validate the data type of dynamic parameters"""
    if param.isalpha():
        return True
    else:
        return False
