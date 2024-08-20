from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user, LoginManager
# from werkzeug.security import generate_password_hash, check_password_hash
from requests.auth import HTTPBasicAuth
import requests
import os

from application.model import User, db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        # Check SNOW to see if user exists
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        url = os.getenv('URL') + "api/now/table/sys_user"
        auth = HTTPBasicAuth(username, password)
        response = requests.get(
            url,
            auth=auth,
            headers={'Accept': 'application/json'}
        )
    
    # Check if the response status code indicates success
    if response.status_code != 200:
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    
    new_user = User.query.get(username) # if this returns a user, then the email already exists in database

    if not new_user: 
        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
    login_user(new_user)

    next_page = request.args.get("next")
    if next_page:
        return redirect(next_page)
    return redirect(url_for('bp.home'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))