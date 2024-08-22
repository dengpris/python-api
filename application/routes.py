from datetime import datetime
from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from requests.auth import HTTPBasicAuth
from application.model import db, Item
import requests
import os
import json

bp = Blueprint('bp', __name__)

headers = {'Content-type': 'application/json'}
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
auth = HTTPBasicAuth(username, password)
# auth = {
#     "client_id": os.getenv('CLIENT_ID'),
#     "client_secret": os.getenv('CLIENT_SECRET')
# }

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
    
    return jsonify({"msg": msg}), 200

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
@login_required
def incident_list():
    url = os.getenv('URL') + '/api/now/v1/table/incident'
    incidents = requests.get(url, auth=auth)
    return incidents.json(), 200

@bp.route("/incident/{id}")
@login_required
def incident_get():
    url = os.getenv('URL') + f'/api/now/v1/table/incident/{id}'
    incident = requests.get(url, auth=auth)
    return incident.json(), 200

@bp.route("/incident/create", methods=['GET', 'POST'])
@login_required
def incident_create():
    url = os.getenv('URL') + 'api/now/v1/table/incident'
    if request.method == "GET":
        return render_template('create_incident.html', callerid=get_callerid(username))
    else:
        data = json.dumps(request.form)
        result = requests.post(url, auth=auth, headers=headers, data=data)
        return result.json(), 201
        # return jsonify(request.form)
    

def get_callerid(username):
    url = os.getenv('URL') + f'/api/now/table/sys_user?sysparm_query=user_name={username}'
    res = requests.get(url, auth=auth)
    
    return res.json()['result'][0]['email']