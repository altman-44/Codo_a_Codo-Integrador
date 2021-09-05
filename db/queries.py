import jwt
import os
from extensions import dbSession
from helpers_session import generateUserTypeData, generateUserTypePayload
from flask import flash
from models.User import User
from models.Organization import Organization
from models.Employee import Employee

def createUser(email, password):
    USER_NOT_CREATED = "Couldn't create user, try it later"
    created = False
    user = dbSession.query(User).filter_by(email=email).first()
    if not user:
        passwordToken = jwt.encode({'password': password}, os.getenv('SECRET_KEY'), algorithm='HS256')
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
    organization = dbSession.query(Organization).filter_by(user_id=userId).first()
    if organization:
        data = generateDataForOrganization(organization)
        payload['organization_id'] = organization.id
        payload['user_type'] = generateUserTypePayload(userType=Organization, id=organization.id)
    else:
        employee = dbSession.query(Employee).filter_by(user_id=userId).first()
        if employee:
            data = generateUserTypeData(userType='employee', details=employee)
            payload['organization_id'] = employee.organization_id
            payload['user_type'] = generateUserTypePayload(userType=Employee, id=employee.id)
    if payload:
        payload['user_id'] = userId
    return (payload, data)

def generateDataForOrganization(organizationData):
    data = generateUserTypeData(userType='organization', details=organizationData)
    return data