from json import load
import os
import secrets
import cloudinary
from dotenv import load_dotenv
from extensions import app
from controller import *

load_dotenv()

# Settings
''' DB '''
# if os.getenv('ENV_MODE') != 'production':
#     app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_CONNECTION_HOST')
#     app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_CONNECTION_USER')
#     app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_CONNECTION_PASSWORD')
#     app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_CONNECTION_DATABASE')
#     db.init_app(app)
''' Session '''
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
''' Cloudinary '''
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)
# ''' Uploads '''
# app.config['UPLOADS_PATH'] = os.path.join('uploads')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True if os.getenv('ENV_MODE') != 'production' else False)
