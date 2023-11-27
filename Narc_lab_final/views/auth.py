from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models import *

auth = Blueprint('auth', __name__)


# Your register, login, logout views here


@auth.route('/login', methods=['GET', 'POST'])
def login():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboards.dashboard'))
        else:
            message = 'Login Unsuccessful. Please check username and password'
            return render_template('login.html', message=message)
    return render_template('login.html', message=message)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
