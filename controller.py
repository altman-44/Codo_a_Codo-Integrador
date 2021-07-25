from werkzeug.wrappers import Response
from extensions import app
from routes.home import home
from routes.employees import employees
from routes.organizations import organizations
from routes.dashboard import dashboard

app.register_blueprint(home)
app.register_blueprint(organizations, url_prefix='/organizations')
app.register_blueprint(employees, url_prefix='/employees')
app.register_blueprint(dashboard, url_prefix='/dashboard')