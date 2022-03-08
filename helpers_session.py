import os
import jwt

def encodeData(payload):
    """A function that encodes a payload to convert it into a token and so store this token in the session variable"""
    payload['auth_secret'] = os.getenv('BASE_AUTH_SECRET')
    return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')

def decodeToken(token):
    return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])

# def generateUserTypeData(userType, details):
#     return {
#         'type': userType,
#         'details': {col.name: getattr(details, col.name) for col in details.__table__.columns}
#     }

def generateUserData(entityInstance):
    return {
        'details': {col.name: getattr(entityInstance, col.name) for col in entityInstance.__table__.columns}
    }

def generateUserDataPayload(userId, organizationId=None):
    return {
        'organization_id': organizationId,
        'user_id': userId
        # 'user_type': {
        #     'type': userType.__name__ if userType else None,
        #     'id': userTypeId
        # }
    }