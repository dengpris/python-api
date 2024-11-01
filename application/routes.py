from datetime import datetime
from flask import Blueprint, request, jsonify, render_template, session
from flask_login import login_required, current_user
from requests.auth import HTTPBasicAuth
from application.model import db, Item
import requests
import os
import json
import time

bp = Blueprint('bp', __name__)

# username = os.getenv('USERNAME')
# password = os.getenv('PASSWORD')
# auth = HTTPBasicAuth(username, password)

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/hello')
def greeting():
    now = datetime.now()
    hour = now.hour
    msg = ""
    if (hour < 12):
        msg = "Good morning!"
    elif (hour < 17):
        msg = "Good afternoon!"
    elif (hour < 21):
        msg = "Good evening!"
    else:
        msg = "You're up late!"
    
    # TODO: add gif of time of day
    
    return jsonify({"msg": msg, "test": "jsakflsjd"}), 200

@bp.route('/wait')
def wait():
    time.sleep(30)  # Sleep for 30 seconds
    return "Response after 40 seconds"

@bp.route('/item-list')
def item_list():
    items = db.session.execute(db.select(Item).order_by(Item.name)).scalars()
    items_list = [item.as_dict() for item in items]
    
    return jsonify(items_list), 200

@bp.route("/item-list/create", methods=["GET", "POST"])
def item_create():
    if request.method == "POST":
        item = Item(
            name=request.form["name"],
            priority=request.form["priority"],
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.as_dict()), 201

    # TODO: Implement GET
    return {}, 400

@bp.route("/incident-list")
# @login_required
def incident_list():
    # Not working in Orchestrate
    url = os.getenv('URL') + '/api/now/v1/table/incident'
    headers = {"Authorization": f"Bearer {session.get('token')}"}
    incidents = requests.get(url, headers=headers)
    return incidents.json()['result'], 200

@bp.route("/incident/<id>")
# @login_required
def incident_get(id):
    url = os.getenv('URL') + f'/api/now/v1/table/incident/{id}'
    headers = {"Authorization": f"Bearer {session.get('token')}"}
    incident = requests.get(url, headers=headers)
    return incident.json()['result'], 200

@bp.route("/incident/create", methods=['GET', 'POST'])
# @login_required
def incident_create():
    request.json['caller_id'] = get_callerid('admin@example.com')
    # url = os.getenv('URL') + 'api/now/v1/table/incident'
    url = os.getenv('URL') + f'/api/now/v1/table/incident'
    auth = {"Authorization": f"Bearer {session.get('token')}"}
    headers = {**request.headers, **auth}
    headers.pop('Host', None)
    # if request.method == "GET":
    #     return render_template('create_incident.html')
    if request.method == "POST":
        result = requests.post(url, headers=headers, json=request.json)
        return result.json()['result'], 201
    

def get_callerid(email):
    url = os.getenv('URL') + f'api/now/table/sys_user?sysparm_query=email=admin@example.com'
    # f'/api/now/table/sys_user?sysparm_query=user_name={username}'
    headers = {"Authorization": f"Bearer {session.get('token')}"}

    res = requests.get(url, headers=headers)
    return res.json()['result'][0]['sys_id']