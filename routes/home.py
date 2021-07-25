from flask import render_template, Blueprint, request, redirect, url_for

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home.html')

@home.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    return redirect(url_for('dashboard.index'))

@home.route('/register', methods=["GET", "POST"])
def register():
    if (request.method == 'GET'):
        return render_template('register.html')