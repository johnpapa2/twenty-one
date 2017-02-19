"""
Created on Feb 18, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine
from db import settings

DeclarativeBase = declarative_base()


def db_connect():
    """Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(URL(**settings.DATABASE), echo=True)


def recreate_db(engine):
    DeclarativeBase.metadata.drop_all(engine)
    DeclarativeBase.metadata.create_all(engine)
