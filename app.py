from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import time
import os
import json
import jwt
from flask_cors import CORS, cross_origin

from application.methods.usermethods import UserMethods
from application.methods.projectmethods import ProjectMethods

from application.utils.extensions import db
from application.utils.exceptions import CustomException
from application.utils.serializers import serialize_one, serialize_many

# Initialize Flask Application
app = Flask(__name__)
cors = CORS(app)
app.config.from_object('application.environment.config')
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)


def validate_token(request):
    token = request.args.get('token')
    print(token)
    if not token:
        return None
    
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    print(data)
    return data




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
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    if (data['user'] != userid):
        return "Invalid user", 403
    

    if (request.method == 'GET'):
        try:
            all_projects = UserMethods().get_all_projects(userid)
            return serialize_many(all_projects)
        except CustomException as e:
            return e.message, e.status_code

    if (request.method == 'POST'):
        try:
            projectname = request.json.get('projectname')
            ProjectMethods().create_project(userid, projectname)
            return "Successfully added", 201
        except CustomException as e:
            return e.message, e.status_code


if __name__ == "__main__":
    app.run(debug=True)
