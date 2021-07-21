from app import app
from routes.home import home
from routes.employees import employees

app.register_blueprint(home)
app.register_blueprint(employees, url_prefix='/employees')
