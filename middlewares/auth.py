import os
from functools import wraps
from flask import session, redirect, url_for, flash
from helpers_session import decodeToken

def user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        payload = getPayload()
        if payload:
            if verifyBaseAuthSecret(payload):
                return f(*args, **kwargs)
        return redirect(url_for('home.login'))
    return decorated_function

def user_type_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        payload = getPayload()
        print('payload', payload)
        if payload:
            print('there is payload')
            if verifyBaseAuthSecret(payload):
                if verifyUserTypeAuthSecret(payload):
                    return f(*args, **kwargs)
                return redirect(url_for('home.selectUserType'))
        return redirect(url_for('home.login'))
    return decorated_function

def getPayload():
    payload = None
    if 'token' in session:
        payload = decodeToken(session['token'])
    return payload

def verifyBaseAuthSecret(payload):
    if 'auth_secret' in payload and 'user_id' in payload:
        return payload['auth_secret'] == os.getenv('BASE_AUTH_SECRET')
    flash('You must be logged in first', 'warning')
    return False

def verifyUserTypeAuthSecret(payload):
    if 'details' in payload and 'type' in payload['details']:
        return bool(payload['type'])
    flash('You need to specify a user type first')
    return False