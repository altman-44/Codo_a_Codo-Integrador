import os
import cloudinary.uploader as cloudinaryUploader
from flask import Blueprint, render_template, request, redirect, url_for, session
from app import app, db
from pymysql import IntegrityError

users = Blueprint('users', __name__)


@users.route('/')
def getUsers():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    users = cursor.fetchall()
    print(users, list(users))
    for user in list(users):
        if not user['profile_img']:
            user['profile_img'] = 'https://res.cloudinary.com/djaci7iml/image/upload/v1626654451/codo-a-codo/base-user-profile-image.jpg'
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
    sql = 'INSERT INTO employees (username, email, name, surname, profile_img) VALUES (%s, %s, %s, %s, %s)'
    if validUserData(request.form):
        data = (request.form['username'], request.form['email'], request.form['name'],
                request.form['surname'], os.getenv('BASE_USER_PROFILE_IMAGE_URL'))
        try:
            cursor.execute(sql, data)
            conn.commit()
        except IntegrityError as err:
            return handlePyMySQLError(err, url_for('users.createUserView'), 'Hubo un error al intentar subir los datos')
        return redirect(url_for('users.getUsers'))
    session['message'] = "Todos los campos son requeridos"
    return redirect(url_for('users.createUserView'))


@users.route('/edit/<int:id>', methods=["GET"])
def editUserView(id):
    return render_template('users/edit.html', userId=id)


@users.route('/edit/<int:id>', methods=["PUT"])
def editUser(id):
    return redirect(url_for('users.getUsers'))

@users.route('/profile-image', methods=["POST"])
def uploadProfileImage():
    conn = db.connect()
    cursor = conn.cursor()
    sql = f'SELECT * FROM employees WHERE id = {request.form["id"]}'
    user = cursor.execute(sql)
    if user:
        print(user)
        result = cloudinaryUploader.upload(
            request.files['profileImage'],
            folder='codo-a-codo/',
            public_id=user.id
        )
        print(result['secure_url'])
        sql = f"UPDATE employees SET profile_img = {result['secure_url']} WHERE id = {user.id}"
    return redirect(url_for('users.editUserView'))


@users.route('/delete/<int:id>', methods=["DELETE"])
def deleteUser(id):
    conn = db.connect()
    cursor = conn.cursor()
    user = cursor.execute(f'SELECT * FROM users WHERE id = {id}')
    if user:
        sql = f'DELETE FROM employees WHERE id = {id}'
        result = cursor.execute(sql)
        conn.commit()
        print(result)
        # os.remove(os.path.join(
        #     app.config['UPLOADS_PATH']), user['profile_img'])
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
