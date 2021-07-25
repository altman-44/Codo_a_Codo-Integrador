import jwt
import os
from extensions import db
from flask import render_template, Blueprint, request, redirect, url_for, flash

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home.html')

@home.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if validLoginData(request.form):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (request.form['email']))
        user = cursor.fetchone()
        if user:
            jwt.decode(user.password, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            return redirect(url_for('dashboard.index'))
        flash('User with the entered email not found', 'error')
    return render_template('login.html')

@home.route('/register', methods=["GET", "POST"])
def register():
    if (request.method == 'GET'):
        return render_template('register.html')
    if validLoginData(request.form):
        conn = db.connect()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE email = %s', (request.form['email']))
        print('user', user)
        flash('Email is already taken', 'error')
    return render_template('register.html')

def validLoginData(data):
    if not data['name'] or not data['email']:
        flash('All fields are required', 'error')
        return False
    return True