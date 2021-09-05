from extensions import dbSession
from flask import render_template, Blueprint, request, redirect, url_for, flash, session
from db.queries import searchDataByUserId, createUser
from helpers_session import encodeData, decodeToken
from models.User import User

home = Blueprint('home', __name__)


@home.route('/')
def index():
    return render_template('home.html')


@home.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if validLoginData(request.form):
        user = dbSession.query(User).filter_by(
            email=request.form['email']).first()
        if user:
            decodedPasswordPayload = decodeToken(user.password)
            if decodedPasswordPayload['password'] == request.form['password']:
                payload, data = searchDataByUserId(userId=user.id)
                if not payload:
                    payload = {'user_id': user.id}
                    session['token'] = encodeData(payload=payload)
                    return redirect(url_for('home.selectUserType'))
                session['token'] = encodeData(payload=payload)
                session['data'] = data
                return redirect(url_for('dashboard.index'))
        flash("Email and password don't match", 'error')
    return render_template('login.html', email=request.form['email'], password=request.form['password'])


@home.route('/register', methods=["GET", "POST"])
def register():
    if (request.method == 'GET'):
        return render_template('register.html')
    if validLoginData(request.form):
        if createUser(request.form['email'], request.form['password'])[0]:
            flash('You registered successfully! You can login now', 'success')
            return redirect(url_for('home.login'))
    return render_template('register.html', email=request.form['email'], password=request.form['password'])


@home.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


@home.route('/select-user-type')
def selectUserType():
    return render_template('select-user-type.html')


def validLoginData(data):
    if not data['email'] or not data['password']:
        flash('All fields are required', 'error')
        return False
    return True
