import os
import cloudinary.uploader as cloudinaryUploader
from middlewares.auth import user_auth
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from extensions import db
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
    return render_template('employees/index.html', employees=employees)


@employees.route('/create', methods=['GET'])
@user_auth
def createEmployeeView():
    return render_template('employees/create.html')


@employees.route('/create', methods=['POST'])
def createEmployee():
    if validEmployeeData(request.form):
        GENERIC_DB_ERR_MSG = 'Hubo un error al intentar subir los datos'
        conn = db.connect()
        cursor = conn.cursor()
        sql = 'INSERT INTO employees (name, email, surname, area, profile_img) VALUES (%s, %s, %s, %s, %s)'
        data = (request.form['name'], request.form['email'],
                request.form['surname'], request.form['area'], os.getenv('BASE_USER_PROFILE_IMAGE_URL'))
        try:
            cursor.execute(sql, data)
            conn.commit()
        except IntegrityError as err:
            return handlePyMySQLError(err, url_for('employees.createEmployeeView'), GENERIC_DB_ERR_MSG)
        except:
            flash(GENERIC_DB_ERR_MSG, 'error')
            return redirect(url_for('employees.createEmployeeView'))
        return redirect(url_for('employees.getEmployees'))
    flash('All fields are required', 'error')
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
    flash("Couldn't find the user")
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
    msg = msgIfNotSpecificError
    if error.args[0] == 1062:
        try:
            msg = f"El campo {error.args[1].split('key')[1].strip()} ya fue elegido por otro usuario"
        except IndexError:
            pass
    flash(msg, 'error')
    return redirect(url_for_redirect)


def validEmployeeData(data):
    if (data['name'] and data['email'] and data['surname']):
        return True
    return False
