from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from my_settings import database

DATABASE = f'mysql+pymysql://{database["DB_USERNAME"]}:{database["DB_PASSWORD"]}@{database["DB_HOST"]}:{database["DB_PORT"]}/{database["DB_DATABASE"]}?charset=utf8'

ENGINE = create_engine(
    DATABASE,
    echo=True
)
session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

Base = declarative_base()
Base.query = session.query_property()
