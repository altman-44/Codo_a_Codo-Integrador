import jwt
import os
from extensions import db
from flask import flash

USER_NOT_CREATED = "Couldn't create user, try it later"

def createUser(email, password):
    userId = -1
    conn = db.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = %s', (email))
    user = cursor.fetchone()
    if not user:
        sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
        data = (email, jwt.encode({'password': password}, os.getenv('SECRET_KEY'), algorithm='HS256'))
        try:
            cursor.execute(sql, data)
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email))
            user = cursor.fetchone()
            if user:
                userId = user['id']
            else:
                flash(USER_NOT_CREATED, 'error')
        except:
            flash(USER_NOT_CREATED, 'error')
    else:
        flash('Email is already taken', 'error')
    return userId