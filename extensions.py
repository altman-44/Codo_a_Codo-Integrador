import os
from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from db.HerokuPostgresql import HerokuPostgresql

app = Flask(__name__, template_folder='templates')

db = ''

if os.getenv('ENV_MODE') == 'production':
    db = HerokuPostgresql(os.getenv('DATABASE_URL'))
else:
    db = MySQL(cursorclass=DictCursor)