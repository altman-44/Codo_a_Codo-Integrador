import os

from pymysql.err import Error
from extensions import app
from pymysql import DatabaseError as MySQLDatabaseError
from psycopg2 import DatabaseError as PostgreSQLDatabaseError
from sqlalchemy.exc import SQLAlchemyError
from flask import request, session, redirect, flash, url_for, render_template
from routes.home import home
# from routes.employees import employees
from routes.students import students
from routes.organizations import organizations
from routes.dashboard import dashboard

MAX_NUMBER_OF_REDIRECTS_TO_REFERRER = 4

app.register_blueprint(home)
app.register_blueprint(organizations, url_prefix='/organizations')
app.register_blueprint(students, url_prefix='/students')
# app.register_blueprint(employees, url_prefix='/employees')
app.register_blueprint(dashboard, url_prefix='/dashboard')

# @app.before_request
# def before_request_func():
#     if request.referrer and request.path[::-1][1:request.path[::-1].find('/')].find('.') == -1:
#         print('-----------------------', flush=True)
#         print('REFERRER: ', request.referrer, flush=True)
#         print('PATH: ', request.path, flush=True)
#         session['referrer'] = request.referrer

# @app.errorhandler(MySQLDatabaseError)
# def mysqlDatabaseError(error):
#     return handleDatabaseError()

# @app.errorhandler(PostgreSQLDatabaseError)
# def postgresqlDatabaseError(error):
#     return handleDatabaseError()

@app.errorhandler(SQLAlchemyError)
def handleSimpleError(error):
    print('DATABASE ERROR', error)
    return handleDatabaseError()

def handleDatabaseError():
    if 'referrer' in session:
        session['referrerCounter'] = (session['referrerCounter'] if 'referrerCounter' in session else 0) + 1
        flash('There was an internal error. Please, try it later.', 'error')
        print('COUNTER: ', session['referrerCounter'], flush=True)
        if session['referrerCounter'] > int(os.getenv('MAX_NUMBER_OF_REDIRECTS_TO_REFERRER') or MAX_NUMBER_OF_REDIRECTS_TO_REFERRER):
            return redirect(url_for('home.index'))
        return redirect(session['referrer'])
    return render_template('server-error.html')