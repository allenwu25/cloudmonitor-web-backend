from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import time
import os
import json
import jwt
from flask_cors import CORS, cross_origin

from application.methods.usermethods import UserMethods
from application.models.user import User
from application.methods.projectmethods import ProjectMethods
from application.methods.targetmethods import TargetMethods
from application.methods.responsemethods import ResponseMethods


from application.utils.extensions import db
from application.utils.exceptions import CustomException
from application.utils.serializers import serialize_one, serialize_many, serialize_dictionary

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
    try:  
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        return data
    except:
        return None

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
        token_and_user = UserMethods().login(email, password)
        return json.dumps(token_and_user), 201

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
        token_and_user = UserMethods().signup(email, password)
        return json.dumps(token_and_user), 201
    
    except CustomException as e:
        return e.message, e.status_code


@app.route('/users/get_user_by_token', methods=['GET'])
@cross_origin()
def get_user_by_token():
    data = validate_token(request)
    if ((data == None) or (data.get('user') == None)): 
        return "Token is invalid or not present", 403
    return json.dumps({'userid': data.get('user')})



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

    elif (request.method == 'POST'):
        try:
            projectname = request.json.get('projectname')
            ProjectMethods().create_project(userid, projectname)
            return "Successfully added", 201
        except CustomException as e:
            return e.message, e.status_code

    else:
        return "Invalid Request Method", 405

# retrieve user information with email (+token)
@app.route('/users/getuser/<email>', methods=['GET'])
@cross_origin()
def user_info(email):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    try:
        user_info = UserMethods().get_user_details(email, remove_password=True)
        return serialize_one(user_info)
    except CustomException as e:
        return e.message, e.status_code

@app.route('/projects/<int:projectid>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def individual_project(projectid):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    if (request.method == 'GET'):
        try:
            existing_project = ProjectMethods().get_project_by_id(projectid, data['user'])
            if (existing_project == None):
                raise CustomException("Project does not exist under userid", 400)
            return serialize_one(existing_project)            
        except CustomException as e:
            return e.message, e.status_code
            
    elif (request.method == 'PUT'):
        try:
            update_parameters = request.json
            ProjectMethods().update_project(projectid, update_parameters, data['user'])
            return "Successfully updated", 201
        except CustomException as e:
            return e.message, e.status_code

    elif (request.method == 'DELETE'):
        try:
            ProjectMethods().delete_project(projectid, data['user'])
            return "Successfully deleted", 201
        except CustomException as e:
            return e.message, e.status_code

    else:
        return "Invalid Request method", 405



@app.route('/projects/<int:projectid>/targets', methods=['GET', 'POST'])
@cross_origin()
def project_targets(projectid):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    if (request.method == 'POST'):
        try:
            target_info = request.json
            TargetMethods().create_target(projectid, data['user'], target_info)
            return "Successfully created target", 201
        except CustomException as e:
            return e.message, e.status_code
    else:
        return "Invalid Request method", 405


@app.route('/projects/<int:projectid>/targets/<int:targetid>', methods=['GET', 'PUT', 'DELETE'])
@cross_origin()
def individual_target(projectid, targetid):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403


    if (request.method == 'PUT'):
        try:
            target_update_info = request.json
            TargetMethods().update_target(projectid, data['user'], targetid, target_update_info)
            return "Successfully updated target", 201
        except CustomException as e:
            return e.message, e.status_code

    elif (request.method == 'DELETE'):
        try:
            TargetMethods().delete_target(projectid, data['user'], targetid)
            return "Successfully deleted target", 201
        except CustomException as e:
            return e.message, e.status_code

    else:
        return "Invalid Request method", 405

# get URLs by projectid
@app.route('/projects/urls/<int:projectid>', methods=['GET'])
@cross_origin()
def project_urls(projectid):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    try:
        urls = ProjectMethods().get_urls(projectid)
        return serialize_many(urls)
    except CustomException as e:
        return e.message, e.status_code

# get individual URL information by urlid
@app.route('/targets/info/<int:urlid>', methods=['GET'])
@cross_origin()
def url_info(urlid):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    try:
        info = TargetMethods().get_target_by_id(urlid)
        return serialize_one(info)
    except CustomException as e:
        return e.message, e.status_code

# get all the response information by urlid
@app.route('/targets/responses/<int:urlid>', methods=['GET'])
@cross_origin()
def url_response_info(urlid):
    data = validate_token(request)
    if data == None: return "Token is invalid or not present", 403

    try:
        responses = ResponseMethods().get_responses_filtered_by_date(urlid)
        return serialize_dictionary(responses)
    except CustomException as e:
        return e.message, e.status_code

if __name__ == "__main__":
    app.run(debug=True)
