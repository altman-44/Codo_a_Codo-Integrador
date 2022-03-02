import os
import cloudinary.uploader as cloudinaryUploader
from middlewares.auth import user_auth, user_type_auth, getPayload
from flask import Blueprint, request, redirect, url_for, flash, jsonify, session
from extensions import dbSession
from routes.general_functions import render_layout_template
from pymysql import IntegrityError
from db.queries import createUser
from models.Employee import Employee
from models.User import User
from helpers.resource_uploader import uploadProfileImage as helper_uploadProfileImage

employees = Blueprint('employees', __name__)


""" This functions is required in order to run the middleware 'user_auth' before every request"""
@employees.before_request
@user_auth
def before_request():
    pass


@employees.route('/')
def getEmployees():
    if session['data']['type'] == 'organization':
        employeesAux = []
        employees = dbSession.query(Employee).filter_by(
            organization_id=session["data"]["details"]["id"]).all()
        for employee in list(employees):
            user = dbSession.query(User).filter_by(
                id=employee.user_id).first()
            employeeAux = employee
            email = user.email
            employeeAux.email = email
            employeesAux.append(employeeAux)
            if not employee.profile_img:
                employee.profile_img = os.getenv(
                    'BASE_USER_PROFILE_IMAGE_URL')
        return render_layout_template('employees/index.html', employees=employeesAux)
    flash("You can't access this view", 'error')
    return redirect(url_for('dashboard.index'))


@employees.route('/create', methods=['GET'])
def createEmployeeView(email='', name='', surname='', area=''):
    return render_layout_template('employees/create.html', email=email, name=name, surname=surname, area=area)


@employees.route('/create', methods=['POST'])
@user_type_auth
def createEmployee():
    """A function to create an employee. Executed by the action of an organization admin, not an employee."""
    if validEmployeeData(request.form):
        GENERIC_DB_ERR_MSG = 'Hubo un error al intentar subir los datos'
        createdUser = createUser(
            request.form['email'], request.form['password'])[1]
        if createdUser:
            payload = getPayload()
            try:
                employee = Employee(request.form['name'], request.form['surname'],
                    payload['user_data']['organization_id'], createdUser.id, request.form['area'])
                dbSession.add(employee)
                dbSession.commit()
                session.pop('_flashes', None)
                flash('User created successfully!', 'success')
            except Exception:
                flash(GENERIC_DB_ERR_MSG, 'error')
                return redirect(url_for('employees.createEmployeeView', email=request.form['email'], name=request.form['name'], surname=request.form['surname'], area=request.form['area']))               
            return redirect(url_for('employees.getEmployees'))
    flash('All fields are required', 'error')
    return redirect(url_for('employees.createEmployeeView', email=request.form['email'], name=request.form['name'], surname=request.form['surname'], area=request.form['area']))


@employees.route('/edit/<int:id>', methods=["GET"])
def editEmployeeView(id):
    employee = dbSession.query(Employee).filter_by(id=id).first()
    if employee:
        employeeAux = employee
        user = dbSession.query(User).filter_by(id=employee.user_id).first()
        employeeAux.email = ''
        if user:
            employeeAux.email = user.email
        if not employeeAux.profile_img:
            employeeAux.profile_img = os.getenv(
            'BASE_USER_PROFILE_IMAGE_URL')            
        return render_layout_template('employees/edit.html', employee=employeeAux)
    flash("Couldn't find the employee", 'error')
    return redirect(url_for('employees.getEmployees'))


@employees.route('/edit/<int:id>', methods=["PUT"])
def editEmployee(id):
    type = 'error'
    employee = dbSession.query(Employee).filter_by(id=id).first()
    if employee:
        try:
            dbSession.query(User).filter_by(id=employee.user_id).update({'email': request.form['email']})
            employee.name = request.form['name']
            employee.surname = request.form['surname']
            employee.area = request.form['area']
            
            dbSession.commit()
            type = 'success'
            message = 'User data was updated successfully'
        except:
            message = 'There was an error trying to update the data. Please, try it later'
    return jsonify(redirect_url=url_for('employees.getEmployees'), type=type, message=message)


@employees.route('/profile-image', methods=["POST"])
def uploadProfileImage():
    employee = dbSession.query(Employee).filter_by(id=request.form['id']).first()
    if employee:
        if request.files['profileImage']:
            result = helper_uploadProfileImage(request.files['profileImage'], employee.user_id)
            employee.profile_img = result['secure_url']
            dbSession.commit()
        else:
            flash('No image was uploaded!', 'error')
            return redirect(url_for('employees.editEmployeeView', id=employee.id))
        return redirect(url_for('employees.getEmployees'))
    return redirect(url_for('home.index'))


@employees.route('/delete/<int:id>', methods=["DELETE"])
def deleteEmployee(id):
    type = 'error'
    message = "Couldn't delete the employee"
    employee = dbSession.query(Employee).filter_by(id=id).first()
    if employee:
        try:
            dbSession.delete(employee)
            dbSession.query(User).filter_by(id=employee.user_id).delete()
            dbSession.commit()
            type = 'success'
            message = f"Employee '{employee.name + ' ' + employee.surname}' removed successfully"
        except:
            pass
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
