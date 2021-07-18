from app import app
from routes.home import home
from routes.users import users

app.register_blueprint(home)
app.register_blueprint(users, url_prefix='/users')
