import os
import cloudinary.uploader as cloudinaryUploader
from middlewares.auth import user_auth, getPayload
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from extensions import db
from pymysql import IntegrityError
from db.queries import createUser

employees = Blueprint('employees', __name__)

@employees.before_request
@user_auth
def before_request():
    pass

@employees.route('/')
def getEmployees():
    conn = db.connect()
    cursor = conn.cursor()
    if session['data']['type'] == 'organization':
        cursor.execute(f'SELECT * FROM employee_accounts WHERE organization_id = {session["data"]["details"]["id"]}')
        employees = cursor.fetchall()
        for employee in list(employees):
            cursor.execute('SELECT email FROM users WHERE users.id = %s', (employee['user_id']))
            user = cursor.fetchone()
            employee['email'] = user['email']
            if not employee['profile_img']:
                employee['profile_img'] = os.getenv('BASE_USER_PROFILE_IMAGE_URL')
        return render_template('employees/index.html', employees=employees)
    flash("You can't access this view", 'error')
    return redirect(url_for('dashboard.index'))

@employees.route('/create', methods=['GET'])
def createEmployeeView(email='', name='', surname='', area=''):
    return render_template('employees/create.html', email=email, name=name, surname=surname, area=area)


@employees.route('/create', methods=['POST'])
def createEmployee():
    if validEmployeeData(request.form):
        GENERIC_DB_ERR_MSG = 'Hubo un error al intentar subir los datos'
        createdUser = createUser(request.form['email'], request.form['password'])[1]
        if createdUser:
            payload = getPayload()
            conn = db.connect()
            cursor = conn.cursor()
            sql = 'INSERT INTO employee_accounts (name, surname, area, profile_img, organization_id, user_id) VALUES (%s, %s, %s, %s, %s, %s)'
            data = (request.form['name'], request.form['surname'], request.form['area'], os.getenv('BASE_USER_PROFILE_IMAGE_URL'), payload['organization_id'], createdUser['id'])
            try:
                cursor.execute(sql, data)
                conn.commit()
            except IntegrityError as err:
                return handlePyMySQLError(err, url_for('employees.createEmployeeView', email=request.form['email'], name=request.form['name'], surname=request.form['surname'], area=request.form['area']), GENERIC_DB_ERR_MSG)
            except:
                flash(GENERIC_DB_ERR_MSG, 'error')
                return redirect(url_for('employees.createEmployeeView', email=request.form['email'], name=request.form['name'], surname=request.form['surname'], area=request.form['area']))
            return redirect(url_for('employees.getEmployees'))
    flash('All fields are required', 'error')
    return redirect(url_for('employees.createEmployeeView', email=request.form['email'], name=request.form['name'], surname=request.form['surname'], area=request.form['area']))


@employees.route('/edit/<int:id>', methods=["GET"])
def editEmployeeView(id):
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM employee_accounts WHERE id={id}')
    employee = cursor.fetchone()
    if employee:
        result = cursor.execute(f"SELECT email FROM users WHERE id={employee['user_id']}")
        if result:
            user = cursor.fetchone()
            employee['email'] = user['email']
        if not employee['profile_img']:
            employee['profile_img'] = os.getenv('BASE_USER_PROFILE_IMAGE_URL')
        return render_template('employees/edit.html', employee=employee)
    flash("Couldn't find the employee")
    return redirect(url_for('employees.getEmployees'))


@employees.route('/edit/<int:id>', methods=["PUT"])
def editEmployee(id):
    type = 'error'
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM employee_accounts WHERE id={id}')
    employee = cursor.fetchone()
    if employee:
        try:
            cursor.execute(f"SELECT * FROM users WHERE id={employee['user_id']}")
            user = cursor.fetchone()

            newName = request.form['name']
            newSurname = request.form['surname']
            newArea = request.form['area']
            userResult = 1
            employeeResult = 1
            
            if user and user['email'] != request.form['email']:
                userResult = cursor.execute(f"UPDATE users SET email='{request.form['email']}' WHERE id={employee['user_id']}")
            if employee['name'] != newName or employee['surname'] != newSurname or employee['area'] != newArea:
                employeeResult = cursor.execute(f"UPDATE employee_accounts SET name='{newName}', surname='{newSurname}', area='{newArea}' WHERE id={id}")
            if userResult and employeeResult:
                type = 'success'
                message = 'User data was updated successfully'
                conn.commit()
            elif userResult:
                type = 'warning'
                message = "User data was updated successfully but the data related to the employee account couldn't be updated"
                conn.commit()
            elif employeeResult:
                type = 'warning'
                message = "The data related to the employee account was updated successfully but the user data couldn't be updated"
                conn.commit()
        except:
            message = 'There was an error trying to update the data. Please, try it later'
    return jsonify(redirect_url=url_for('employees.getEmployees'), type=type, message=message)

@employees.route('/profile-image', methods=["POST"])
def uploadProfileImage():
    conn = db.connect()
    cursor = conn.cursor()
    sql = f'SELECT * FROM employee_accounts WHERE id = {request.form["id"]}'
    cursor.execute(sql)
    employee = cursor.fetchone()
    if employee:
        result = cloudinaryUploader.upload(
            request.files['profileImage'],
            folder='codo-a-codo/',
            public_id=employee['id']
        )
        sql = f"UPDATE employee_accounts SET profile_img = '{result['secure_url']}' WHERE id = {employee['id']}"
        cursor.execute(sql)
        conn.commit()
        return redirect(url_for('employees.editEmployeeView', id=employee['id']))
    return redirect(url_for('home.index'))

@employees.route('/delete/<int:id>', methods=["DELETE"])
def deleteEmployee(id):
    type = 'error'
    message = "Couldn't delete the employee"
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM employee_accounts WHERE id = {id}')
    employee = cursor.fetchone()
    if employee:
        # sql = f'DELETE FROM employee_accounts WHERE id = {id}'
        result = cursor.execute(f"DELETE FROM users WHERE id={employee['user_id']}")
        if result:
            conn.commit()
            type = 'success'
            message = f"Employee '{employee['name'] + ' ' + employee['surname']}' removed successfully"
    redirectUrl = url_for('employees.getEmployees')
    return jsonify(redirect_url=redirectUrl, type=type, message=message)


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
