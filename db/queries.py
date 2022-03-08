import jwt
import os
from extensions import dbSession
from helpers_session import generateUserDataPayload, generateUserData
from flask import flash
from models.User import User
from models.Organization import Organization


def createUser(email, password):
    USER_NOT_CREATED = "Couldn't create user, try it later"
    created = False
    user = dbSession.query(User).filter_by(email=email).first()
    if not user:
        passwordToken = jwt.encode(
            {'password': password}, os.getenv('SECRET_KEY'), algorithm='HS256')
        try:
            user = User(email, passwordToken)
            dbSession.add(user)
            dbSession.commit()
            created = True
        except:
            flash(USER_NOT_CREATED, 'error')
    else:
        flash('Email is already taken', 'error')
    return (created, user)


def searchDataByUserId(userId):
    payload = {}
    data = None
    organization = dbSession.query(
        Organization).filter_by(user_id=userId).first()
    if organization:
        payload['user_data'] = generateUserDataPayload(
            userId=userId,
            organizationId=organization.id
        )
        data = generateUserData(organization)
    return (payload, data)
