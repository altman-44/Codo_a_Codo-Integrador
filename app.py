from controller import *
import os
import secrets
import cloudinary
from db.HerokuPostgresql import HerokuPostgresql
from flask import Flask
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from routes.home import home
from routes.employees import employees

app = Flask(__name__, template_folder='templates')

db = ''

# Settings
if os.getenv('ENV_MODE') == 'production':
    db = HerokuPostgresql(os.getenv('DATABASE_URL'))
else:
    db = MySQL(cursorclass=DictCursor)
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_CONNECTION_HOST')
    app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_CONNECTION_USER')
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_CONNECTION_PASSWORD')
    app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_CONNECTION_DATABASE')
    db.init_app(app)
''' Session '''
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
''' Cloudinary '''
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)
# ''' Uploads '''
# app.config['UPLOADS_PATH'] = os.path.join('uploads')

''' Routing '''
app.register_blueprint(home)
app.register_blueprint(employees, url_prefix='/employees')

if __name__ == '__main__':
    app.run()
