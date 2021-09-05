import os
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from db.HerokuPostgresql import HerokuPostgresql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

database = ''
SQLALCHEMY_DATABASE_URI = ''

if os.getenv('ENV_MODE') == 'production':
    database = HerokuPostgresql(os.getenv('DATABASE_URL'))
else:
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://root@localhost:3306/{os.getenv('MYSQL_CONNECTION_DATABASE')}?charset=utf8mb4"
    # database = MySQL(cursorclass=DictCursor)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
