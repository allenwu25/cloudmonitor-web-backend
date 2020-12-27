from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
import time
import os
import json
from flask_cors import CORS, cross_origin

from application.utils.extensions import db

from application.models.user import User

# Initialize Flask Application
app = Flask(__name__)
cors = CORS(app)
app.config.from_object('application.environment.config')
app.config.from_pyfile('config.py', silent=True)
db.init_app(app)


@app.route('/')
def start():
    return "Application running"


@app.route('/testdb')
def testdb():
    results = User.query.all()

    final = [res.to_dict() for res in results]

    return json.dumps(final)


if __name__ == "__main__":
    app.run(debug=True)
