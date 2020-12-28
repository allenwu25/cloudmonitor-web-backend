from application.models.user import User
from application.models.project import Project
from application.utils.exceptions import CustomException
from application.utils.extensions import db
from application.environment import config

import jwt, hashlib, datetime

class UserMethods:

    # Gets details for a user given email
    def get_user_details(self, email):
        user_info = User.query.filter(User.email == email).first()
        return user_info


    # Logs a user in given email and password
    def login(self, email, password):

        # Ensure user is registered
        existing_user = self.get_user_details(email)
        if (existing_user == None):
            raise CustomException("User not registered", 401)

        # Check that hashing the password entered matches what's in the database
        bytesval = bytes(password, 'utf-8')
        hashed_entered_password = hashlib.sha256(bytesval).hexdigest()

        if (hashed_entered_password != existing_user.password):
            raise CustomException("Incorrect password", 401)

        # Otherwise we know that user is valid, so create a jwt token
        token = jwt.encode({'user' : email, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1)}, config.SECRET_KEY)
        return token


    # Creates new account for user given email, password
    def signup(self, email, password):

        # Ensure user is a new user
        existing_user = self.get_user_details(email)
        if (existing_user != None):
            raise CustomException("User is already registered", 422)

        # If the user is new, hash their password and create new user record in database
        bytesval = bytes(password, 'utf-8')
        hashed_entered_password = hashlib.sha256(bytesval).hexdigest()
        
        newuser = User(
            email=email,
            password=hashed_entered_password,
            datejoined = datetime.datetime.now()
        )

        db.session.add(newuser)
        db.session.commit()

        # Create new jwt token and return
        token = jwt.encode({'user' : email, 'exp' : datetime.datetime.now() + datetime.timedelta(days=1)}, config.SECRET_KEY)
        return token



    def get_all_projects(self, userid):
        all_projects = Project.query.filter(Project.userid == userid).all()
        return all_projects
    
    
        
        