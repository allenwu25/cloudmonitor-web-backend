from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import time
import os
import json
from flask_cors import CORS, cross_origin

from application.utils.extensions import db
from application.methods.usermethods import UserMethods

from application.utils.exceptions import CustomException

# Initialize Flask Application
app = Flask(__name__)
cors = CORS(app)
app.config.from_object('application.environment.config')
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated



@app.route('/')
@cross_origin()
def start():
    return "Application running"


@app.route('/testdb')
@cross_origin()
def testdb():
    results = User.query.all()

    final = [res.to_dict() for res in results]

    return json.dumps(final)


@app.route('/users/login', methods=['POST'])
@cross_origin()
def login():
    try:
        email = request.json['email']
        password = request.json['password']
    except:
        return "Invalid body parameters", 400
    
    try:
        jwt_token = UserMethods().login(email, password)
        return json.dumps({'token': jwt_token}), 201

    except CustomException as e:
        return e.message, e.status_code



@app.route('/users/signup', methods=['POST'])
@cross_origin()
def signup():
    try:
        email = request.json['email']
        password = request.json['password']
    except:
        return "Invalid body parameters", 400
    
    try:
        jwt_token = UserMethods().signup(email, password)
        return json.dumps({'token': jwt_token}), 201
    
    except CustomException as e:
        return e.message, e.status_code


@app.route('/users/<int:userid>/projects', methods=['GET', 'POST'])
@cross_origin()
def user_projects(userid):
    if (request.method == 'GET'):
        pass
    if (request.method == 'POST'):
        pass


if __name__ == "__main__":
    app.run(debug=True)
