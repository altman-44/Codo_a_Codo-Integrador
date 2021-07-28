import os
import jwt
from extensions import db
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from middlewares.auth import user_auth, getPayload
from helpers_session import generateUserTypeData, encodeData, generateUserTypePayload

organizations = Blueprint('organizations', __name__)

@organizations.before_request
@user_auth
def before_request():
    pass

@organizations.route('/')
def index(organizationName=''):
    return render_template('organizations/create.html', name=organizationName)

@organizations.route('/create', methods=["POST"])
def createOrganization():
    if validOrganizationData(request.form):
        conn = db.connect()
        cursor = conn.cursor()
        payload = getPayload()
        sql = 'INSERT INTO organization_accounts (name, user_id) VALUES (%s, %s)'
        data = (request.form['name'], payload['user_id'])
        try:
            cursor.execute(sql, data)
            conn.commit()
            cursor.execute('SELECT * FROM organization_accounts WHERE name = %s and user_id = %s', (request.form['name'], payload['user_id']))
            data = cursor.fetchone()
            data = generateUserTypeData(userType='organization', details=data)
            payload['user_type'] = generateUserTypePayload(userType='organization', details=data)
            session['token'] = encodeData(payload=payload)
            return redirect(url_for('dashboard.index', data=data))
        except:
            flash('There was an error trying to upload the data', 'error')
    return redirect(url_for('organizations.index', organizationName=request.form['name']))

def validOrganizationData(data):
    if 'name' not in data or not data['name']:
        flash('All fields are required', 'error')
        return False
    return True