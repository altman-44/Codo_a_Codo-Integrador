import os
import secrets
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__, template_folder='templates')

# Settings
''' MySQL '''
db = MySQL()
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_CONNECTION_HOST')
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_CONNECTION_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_CONNECTION_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_CONNECTION_DATABASE')
db.init_app(app)
''' Session '''
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
''' Uploads '''
app.config['UPLOADS_PATH'] = os.path.join('uploads')

from controller import *

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)