from models.Organization import Organization
from extensions import dbSession
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from middlewares.auth import user_auth, getPayload
from helpers_session import encodeData, generateUserData, generateUserDataPayload

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
        payload = getPayload()
        try:
            userId = payload['user_data']['user_id']
            organization = Organization(request.form['name'], userId)
            dbSession.add(organization)
            dbSession.commit()
            payload['user_data'] = generateUserDataPayload(
                userId=userId,
                organizationId=organization.id
            )
            data = generateUserData(entityInstance=organization)
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