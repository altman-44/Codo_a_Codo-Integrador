from extensions import db
from flask import Blueprint, render_template, request, redirect, session, url_for, g

organizations = Blueprint('organizations', __name__)

@organizations.route('/')
def index():
    message = session['message'] if 'message' in session else ''
    return render_template('organizations/create.html', message=message)

@organizations.route('/create', methods=["POST"])
def createOrganization():
    if validateOrganizationData(request.form):
        sql = 'INSERT INTO organizations (name, email) VALUES (%s, %s)'
        data = (request.form['name'], request.form['email'])
        conn = db.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, data)
            conn.commit()
            return redirect(url_for('dashboard.index'))
        except:
            session['message'] = 'Hubo un error al intentar subir los datos'
    return redirect(url_for('organizations.index'))

def validateOrganizationData(data):
    if not data['name'] or not data['email']:
        session['message'] = 'El nombre y el email son requeridos'
        g.message = 'MENSAJE'
        return False
    return True