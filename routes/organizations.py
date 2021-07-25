from extensions import db
from db.helpers import createUser
from flask import Blueprint, render_template, request, redirect, session, url_for, flash

organizations = Blueprint('organizations', __name__)

@organizations.route('/')
def index():
    return render_template('organizations/create.html')

@organizations.route('/create', methods=["POST"])
def createOrganization():
    if validOrganizationData(request.form):
        conn = db.connect()
        cursor = conn.cursor()
        userId = createUser(request.form['email'], request.form['password'])
        sql = 'INSERT INTO organizations (name, user_id) VALUES (%s, %s)'
        data = (request.form['name'], userId)
        try:
            cursor.execute(sql, data)
            conn.commit()
            return redirect(url_for('dashboard.index'))
        except:
            flash('There was an error trying to upload the data', 'error')
    return redirect(url_for('organizations.index'))

def validOrganizationData(data):
    if not data['name'] or not data['email']:
        flash('All fields are required', 'error')
        return False
    return True