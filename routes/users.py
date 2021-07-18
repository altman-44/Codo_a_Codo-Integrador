import os
from flask import Blueprint, render_template, request, redirect, url_for, session
from app import app, db
from pymysql import IntegrityError

users = Blueprint('users', __name__)

@users.route('/')
def getUsers():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    message = session['message'] if 'message' in session else ''
    return render_template('users/index.html', users=users, message=message)

@users.route('/create', methods=['GET'])
def createUserView():
    message = ''
    if ('message' in session):
        message = session['message']
    return render_template('users/create.html', message=message)

@users.route('/create', methods=['POST'])
def createUser():
    conn = db.connect()
    cursor = conn.cursor()
    sql = 'INSERT INTO users (username, email, name, surname) VALUES (%s, %s, %s, %s)'
    if validUserData(request.form):
        data = (request.form['username'], request.form['email'], request.form['name'], request.form['surname'])
        try:
            cursor.execute(sql, data)
            conn.commit()
        except IntegrityError as err:
            return handlePyMySQLError(err, url_for('users.createUserView'), 'Hubo un error al intentar subir los datos')
        return redirect(url_for('users.getUsers'))
    session['message'] = "Todos los campos son requeridos"
    return redirect(url_for('users.createUserView'))

@users.route('/delete/<int:id>', methods=["DELETE"])
def deleteUser(id):
    conn = db.connect()
    cursor = conn.cursor()
    user = cursor.execute(f'SELECT * FROM users WHERE id = {id}')
    if user:
        sql = f'DELETE FROM users WHERE id = {id}'
        cursor.execute(sql)
        conn.commit()
        os.remove(os.path.join(app.config['UPLOADS_PATH']), user['profile_img'])
    return redirect(url_for('users.getUsers'))

def handlePyMySQLError(error, url_for_redirect, msgIfNotSpecificError):
    session['message'] = msgIfNotSpecificError
    if error.args[0] == 1062:
        try:
            session['message'] = f"El campo {error.args[1].split('key')[1].strip()} ya fue elegido por otro usuario"
        except IndexError:
            pass
    return redirect(url_for_redirect)

def validUserData(data):
    if (data['username'] and data['email'] and data['name'] and data['surname']):
        return True
    return False