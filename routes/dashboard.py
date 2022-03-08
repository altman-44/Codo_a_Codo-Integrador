from middlewares.auth import user_auth, getPayload
from flask import Blueprint, render_template, session

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
def index():
    data = None
    if 'data' in session:
        data = session['data']
        # session.pop('data')
    return render_template('dashboard/index.html', data=data)