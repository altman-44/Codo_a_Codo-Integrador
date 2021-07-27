import jwt
import os
from extensions import db
from helpers_session import generateUserTypeData, generateUserTypePayload
from flask import flash

def createUser(email, password):
    USER_NOT_CREATED = "Couldn't create user, try it later"
    created = False
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email))
    user = cursor.fetchone()
    if not user:
        sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
        passwordToken = jwt.encode({'password': password}, os.getenv('SECRET_KEY'), algorithm='HS256')
        data = (email, passwordToken)
        try:
            cursor.execute(sql, data)
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email))
            user = cursor.fetchone()
            if user:
                created = True
            else:
                flash(USER_NOT_CREATED, 'error')
        except:
            flash(USER_NOT_CREATED, 'error')
    else:
        flash('Email is already taken', 'error')
    return (created, user)

def searchDataByUserId(userId):
    payload = {}
    data = None
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM organizations INNER JOIN users ON organizations.user_id = %s', (userId))
    result = cursor.fetchone()
    if result:
        data = generateDataForOrganization(result)
        payload['organization_id'] = result['id']
        payload['user_type'] = generateUserTypePayload(table='organizations', id=result['id'])
    else:
        cursor.execute('SELECT * FROM employees INNER JOIN users ON employees.user_id = %s', (userId))
        data = cursor.fetchone()
        if data:
            data = generateUserTypeData(userType='employee', details=data)
            payload['organization_id'] = result['organization_id']
            payload['user_type'] = generateUserTypePayload(table='employees', id=result['id'])
    if payload:
        payload['user_id'] = userId
    return (payload, data)

def generateDataForOrganization(organizationData):
    data = generateUserTypeData(userType='organization', details=organizationData)
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT email from users INNER JOIN (SELECT * FROM employees WHERE organization_id = %s) AS employees ON employees.user_id = users.id', (organizationData['id']))
    data['employees'] = cursor.fetchall()
    print('employees', data['employees'])
    return data