import os
from functools import wraps
from flask import session, redirect, url_for, flash, request
from helpers_session import decodeToken

def user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        payload = getPayload()
        if payload:
            if verifyBaseAuthSecret(payload):
                return f(*args, **kwargs)
        # redirectToUrl is going to be an url param which will determine what page the user will be redirected to after login
        return redirect(url_for('home.login', redirectToUrl=request.path))
    return decorated_function

# def user_type_auth(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         payload = getPayload()
#         if payload:
#             if verifyBaseAuthSecret(payload):
#                 if verifyUserTypeAuthSecret(payload):
#                     return f(*args, **kwargs)
#                 return redirect(url_for('home.selectUserType'))
#         return redirect(url_for('home.login'))
#     return decorated_function

def getPayload():
    payload = None
    if 'token' in session:
        payload = decodeToken(session['token'])
    return payload

def verifyBaseAuthSecret(payload):
    if 'auth_secret' in payload and 'user_data' in payload and 'user_id' in payload['user_data']:
        return payload['auth_secret'] == os.getenv('BASE_AUTH_SECRET')
    flash('You must be logged in first', 'warning')
    return False

# def verifyUserTypeAuthSecret(payload):
#     if 'user_type' in payload['user_data']:
#         userTypeData = payload['user_data']['user_type']
#         if 'type' in userTypeData and 'id' in userTypeData:
#             return bool(userTypeData['type'] and userTypeData['id'])
#     flash('You need to specify a user type first')
#     return False