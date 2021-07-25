from functools import wraps
from flask import session, redirect, url_for

def user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'organization' not in session:
            session['message'] = 'You must login first'
            return redirect(url_for('home.login'))
        return f(*args, **kwargs)
    return decorated_function