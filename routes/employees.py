import os
import cloudinary.uploader as cloudinaryUploader
from flask import Blueprint, render_template, request, redirect, url_for, session
from app import db
from pymysql import IntegrityError

employees = Blueprint('employees', __name__)


@employees.route('/')
def getEmployees():
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    employees = cursor.fetchall()
    for employee in list(employees):
        if not employee['profile_img']:
            employee['profile_img'] = os.getenv('BASE_USER_PROFILE_IMAGE_URL')
    message = session['message'] if 'message' in session else ''
    return render_template('employees/index.html', employees=employees, message=message)


@employees.route('/create', methods=['GET'])
def createEmployeeView():
    message = ''
    if ('message' in session):
        message = session['message']
    return render_template('employees/create.html', message=message)


@employees.route('/create', methods=['POST'])
def createEmployee():
    conn = db.connect()
    cursor = conn.cursor()
    sql = 'INSERT INTO employees (name, email, surname, area, profile_img) VALUES (%s, %s, %s, %s, %s)'
    if validEmployeeData(request.form):
        data = (request.form['name'], request.form['email'],
                request.form['surname'], request.form['area'], os.getenv('BASE_USER_PROFILE_IMAGE_URL'))
        try:
            cursor.execute(sql, data)
            conn.commit()
        except IntegrityError as err:
            return handlePyMySQLError(err, url_for('employees.createEmployeeView'), 'Hubo un error al intentar subir los datos')
        return redirect(url_for('employees.getEmployees'))
    session['message'] = "Todos los campos son requeridos"
    return redirect(url_for('employees.createEmployeeView'))


@employees.route('/edit/<int:id>', methods=["GET"])
def editEmployeeView(id):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM employees WHERE id={id}')
    employee = cursor.fetchone()
    if employee:
        if not employee['profile_img']:
            employee['profile_img'] = os.getenv('BASE_USER_PROFILE_IMAGE_URL')
        return render_template('employees/edit.html', employee=employee)
    session['message'] = "Couldn't found the user"
    return redirect(url_for('employees.getEmployees'))


@employees.route('/edit/<int:id>', methods=["PUT"])
def editEmployee(id):
    return redirect(url_for('employees.getEmployees'))

@employees.route('/profile-image', methods=["POST"])
def uploadProfileImage():
    conn = db.connect()
    cursor = conn.cursor()
    sql = f'SELECT * FROM employees WHERE id = {request.form["id"]}'
    cursor.execute(sql)
    employee = cursor.fetchone()
    if employee:
        result = cloudinaryUploader.upload(
            request.files['profileImage'],
            folder='codo-a-codo/',
            public_id=employee['id']
        )
        sql = f"UPDATE employees SET profile_img = '{result['secure_url']}' WHERE id = {employee['id']}"
        cursor.execute(sql)
        conn.commit()
        return redirect(url_for('employees.editEmployeeView', id=employee['id']))
    return redirect(url_for('home.index'))

@employees.route('/delete/<int:id>', methods=["DELETE"])
def deleteEmployee(id):
    conn = db.connect()
    cursor = conn.cursor()
    employee = cursor.execute(f'SELECT * FROM employees WHERE id = {id}')
    if employee:
        sql = f'DELETE FROM employees WHERE id = {id}'
        result = cursor.execute(sql)
        conn.commit()
        print(result)
        # os.remove(os.path.join(
        #     app.config['UPLOADS_PATH']), employee['profile_img'])
    return redirect(url_for('employees.getEmployees'))


def handlePyMySQLError(error, url_for_redirect, msgIfNotSpecificError):
    session['message'] = msgIfNotSpecificError
    if error.args[0] == 1062:
        try:
            session['message'] = f"El campo {error.args[1].split('key')[1].strip()} ya fue elegido por otro usuario"
        except IndexError:
            pass
    return redirect(url_for_redirect)


def validEmployeeData(data):
    if (data['name'] and data['email'] and data['surname']):
        return True
    return False
