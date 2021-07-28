from middlewares.auth import user_auth, user_type_auth, getPayload
from extensions import db
from flask import Blueprint, render_template, session

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@user_type_auth
def index():
    data = None
    if 'data' in session:
        data = session['data']
        # session.pop('data')
    print(data)
    return render_template('dashboard/index.html', data=data)