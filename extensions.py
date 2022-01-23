from flask import Flask
from db.connection import session as dbSession

app = Flask(__name__, template_folder='templates')

dbSession = dbSession