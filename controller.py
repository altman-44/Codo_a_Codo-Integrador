import os

from extensions import app
from sqlalchemy.exc import SQLAlchemyError
from flask import session, redirect, flash, url_for, render_template
from routes.home import home
from routes.students import students
from routes.organizations import organizations
from routes.dashboard import dashboard

MAX_NUMBER_OF_REDIRECTS_TO_REFERRER = 4

app.register_blueprint(home)
app.register_blueprint(organizations, url_prefix='/organizations')
app.register_blueprint(students, url_prefix='/students')
app.register_blueprint(dashboard, url_prefix='/dashboard')

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