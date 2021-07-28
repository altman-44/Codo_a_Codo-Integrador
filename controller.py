import os
from extensions import app
from pymysql import DatabaseError as MySQLDatabaseError
from psycopg2 import DatabaseError as PostgreSQLDatabaseError
from flask import request, session, redirect, flash, url_for, render_template
from routes.home import home
from routes.employees import employees
from routes.organizations import organizations
from routes.dashboard import dashboard

MAX_NUMBER_OF_REDIRECTS_TO_REFERRER = 4

app.register_blueprint(home)
app.register_blueprint(organizations, url_prefix='/organizations')
app.register_blueprint(employees, url_prefix='/employees')
app.register_blueprint(dashboard, url_prefix='/dashboard')

@app.before_request
def before_request():
    if request.referrer:
        session['referrer'] = request.referrer

@app.errorhandler(MySQLDatabaseError)
def mysqlDatabaseError(error):
    return handleDatabaseError()

@app.errorhandler(PostgreSQLDatabaseError)
def postgresqlDatabaseError(error):
    return handleDatabaseError()

def handleDatabaseError():
    if 'referrer' in session:
        session['referrerCounter'] = (session['referrerCounter'] if 'referrerCounter' in session else 0) + 1
        flash('There was an internal error. Please, try it later.', 'error')
        if session['referrerCounter'] > int(os.getenv('MAX_NUMBER_OF_REDIRECTS_TO_REFERRER') or MAX_NUMBER_OF_REDIRECTS_TO_REFERRER):
            return redirect(url_for('home.index'))
        return redirect(session['referrer'])
    return render_template('server-error.html')