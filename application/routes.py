from datetime import datetime
from flask import Blueprint, request, jsonify
from requests.auth import HTTPBasicAuth
from application.model import db, Item
import requests
import os

bp = Blueprint('bp', __name__)

auth = HTTPBasicAuth(os.getenv('USERNAME'), os.getenv('PASSWORD'))

@bp.route('/')
def home():
    return "hello world"

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

@bp.route("/incident")
def incident_list():
    url = os.getenv('URL') + '/api/now/v1/table/incident'
    incidents = requests.get(url, auth=auth)
    return incidents.json(), 201