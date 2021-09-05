import os
import jwt

def encodeData(payload):
    payload['auth_secret'] = os.getenv('BASE_AUTH_SECRET')
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

def decodeToken(token):
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

def generateUserTypeData(userType, details):
    return {
        'type': userType,
        'details': {col.name: getattr(details, col.name) for col in details.__table__.columns}
    }

def generateUserTypePayload(userType, id):
    return {
        'type': userType.__name__,
        'id': id
    }