from application.utils.extensions import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'Users'
    id = db.Column('Userid', db.Integer, primary_key=True)
    email = db.Column('Email', db.String(500))
    password = db.Column('Password', db.String(500))
    datejoined = db.Column('DateJoined', db.DateTime)


