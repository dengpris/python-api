from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from requests.auth import HTTPBasicAuth
import requests
import os

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
    
    return "Success", 200

