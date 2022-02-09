import os
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from db.HerokuPostgresql import HerokuPostgresql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# database = ''
SQLALCHEMY_DATABASE_URI = ''

if os.getenv('ENV_MODE') == 'production':
    # database = HerokuPostgresql(os.getenv('DATABASE_URL'))
    SQLALCHEMY_DATABASE_URI = os.getenv('PROD_SQL_ALCHEMY_DATABASE_URI')
else:
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_SQL_ALCHEMY_DATABASE_URI')
    # database = MySQL(cursorclass=DictCursor)

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
