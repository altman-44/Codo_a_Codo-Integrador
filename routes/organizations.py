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
        print(payload)
        sql = f"INSERT INTO organization_accounts (name, user_id) VALUES ('{request.form['name']}', {payload['user_id']})"
        # data = (request.form['name'], payload['user_id'])
        try:
            # cursor.execute(sql, data)
            cursor.execute(sql)
            conn.commit()
            cursor.execute(f"SELECT * FROM organization_accounts WHERE name = '{request.form['name']}' and user_id = {payload['user_id']}")
            data = cursor.fetchone()
            payload['organization_id'] = data['id']
            data = generateUserTypeData(userType='organization', details=data)
            payload['user_type'] = generateUserTypePayload(table='organization_accounts', id=data['details']['id'])
            session['token'] = encodeData(payload=payload)
            session['data'] = data
            return redirect(url_for('dashboard.index'))
        except:
            flash('There was an error trying to upload the data', 'error')
    return redirect(url_for('organizations.index', organizationName=request.form['name']))

def validOrganizationData(data):
    if 'name' not in data or not data['name']:
        flash('All fields are required', 'error')
        return False
    return True