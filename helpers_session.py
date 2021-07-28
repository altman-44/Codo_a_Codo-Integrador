import os
import jwt

def encodeData(payload):
    payload['auth_secret'] = os.getenv('BASE_AUTH_SECRET')
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

def decodeToken(token):
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

def generateUserTypeData(userType='', details={}):
    return {
        'type': userType,
        'details': dict(details)
    }

def generateUserTypePayload(table='', id=None):
    return {
        'table': table,
        'id': id
    }