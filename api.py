from flask import Flask, jsonify, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return "hello world"

@app.route('/hello')
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
    
    return jsonify({"msg": msg}), 200



# Run flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)