import os
# import cloudinary.uploader as cloudinaryUploader
from middlewares.auth import user_auth, getPayload
from flask import Blueprint, request, redirect, url_for, flash, jsonify, session
from extensions import dbSession
from routes.general_functions import render_layout_template
from db.queries import createUser
from models.Student import Student
""" These imports must be here so that SQLAlchemy can identify and use each entity """
from models.StudentOrigin import StudentOrigin
from models.Location import Location
from models.StudentContact import StudentContact
""""""
# from models.User import User
from helpers.resource_uploader import uploadProfileImage as helper_uploadProfileImage


students = Blueprint('students', __name__)
@students.before_request
@user_auth
def before_request():
    pass

@students.route('/')
def getStudents():
    students = dbSession.query(Student).filter_by(
        organizationId=session["data"]["details"]["id"]).all()
    return render_layout_template('students/index.html', students=students)


@students.route('/create', methods=['GET'])
def addStudentView(email='', name='', surname=''):
    return render_layout_template('students/add.html', email=email, name=name, surname=surname)


@students.route('/create', methods=['POST'])
def addStudent():
    """A function to create an employee. Executed by the action of an organization admin, not an employee."""
    GENERIC_DB_ERR_MSG = 'Hubo un error al intentar subir los datos'
    print(*request.form)
    
    payload = getPayload()
    try:
        # data = {
        #     'name': request.form['name'],
        #     'surname': request.form['surname'],
        #     'entryDate': request.form['entryDate'],
        #     request.form['year'],
        #     request.form['school'],
        #     request.form['phone'],
        #     request.form['recommendedBy'] if 'recommendedBy' in request.form else None
        # }
        # student = Student(
        #     payload['user_data']['organization_id'],
        #     *data
        # )
        # dbSession.add(student)
        # dbSession.commit()
        # session.pop('_flashes', None)
        flash('User created successfully!', 'success')
    except Exception:
        flash(GENERIC_DB_ERR_MSG, 'error')
        return redirect(url_for('students.addStudentView', **request.form))               
    return redirect(url_for('students.getStudents'))
    # return redirect(url_for('students.addStudentView', name=request.form['name'], surname=request.form['surname']))


@students.route('/edit/<int:id>', methods=["GET"])
def editStudentView(id):
    student = dbSession.query(Student).filter_by(id=id).first()
    if student:         
        return render_layout_template('students/edit.html', student=student)
    flash("Couldn't find the employee", 'error')
    return redirect(url_for('students.getStudents'))


@students.route('/edit/<int:id>', methods=["PUT"])
def editStudent(id):
    type = 'error'
    student = dbSession.query(Student).filter_by(id=id).first()
    if student:
        try:
            student.name = request.form['name']
            student.surname = request.form['surname']
            student.school = request.form['area']
            student.entryDate = request.form['entryDate']
            dbSession.commit()
            type = 'success'
            message = 'User data was updated successfully'
        except:
            message = 'There was an error trying to update the data. Please, try it later'
    return jsonify(redirect_url=url_for('students.getStudents'), type=type, message=message)


@students.route('/delete/<int:id>', methods=["DELETE"])
def deleteStudent(id):
    type = 'error'
    message = "Couldn't delete the student"
    student = dbSession.query(Student).filter_by(id=id).first()
    if student:
        try:
            dbSession.delete(student)
            dbSession.commit()
            type = 'success'
            message = f"Alumno '{student.name + ' ' + student.surname}' eliminado exitosamente"
        except:
            pass
    redirectUrl = url_for('students.getStudents')
    return jsonify(redirect_url=redirectUrl, type=type, message=message)
