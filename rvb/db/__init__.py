import os
from sqlalchemy import create_engine, exc
from sqlalchemy.engine.url import URL
from rvb.db.config import DATABASE

def parse_url(database):
    """
    Converts a db config dictionairy into an acceptable
    connection string.
    """
    if database and database['password']:
        # Assuming Remote
        return URL(**database)
    elif database:
        # Assuming Local
        return 'postgresql:///' + database['database']
    else:
        # Assuming Master Set Up
        return 'postgresql:///postgres'

def connect(database):
    """
    Performs database connection using database settings from db_config.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(parse_url(database))

def create(engine, database):
    """
    Creates database
    """
    connection = engine.connect()
    connection.execute("commit")
    try:
        connection.execute("create database {db_name}".format(db_name=database['database']))
    except exc.ProgrammingError:
        print("Database Already Exists!")
    except:
        print("DB create failed!")
        raise
    finally:
        connection.close()

def drop(engine, database):
    """
    Drops database
    """
    connection = engine.connect()
    connection.execute("commit")
    try:
        connection.execute("drop database {db_name}".format(db_name=database['database']))
    except exc.ProgrammingError:
        print("Database Does Not Exist!")
    except:
        print("DB drop failed!")
        raise
    finally:
        connection.close()
