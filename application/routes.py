from datetime import datetime
from flask import Blueprint, request, jsonify

bp = Blueprint('bp', __name__)

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

@bp.route('/todo-list', methods=['GET', 'POST'])
def todo_list():
    if request.method == 'GET':
        return 0
    elif request.method == 'POST':
        return 0
