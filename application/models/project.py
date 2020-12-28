from application.utils.extensions import db
from sqlalchemy_serializer import SerializerMixin

class Project(db.Model, SerializerMixin):
    __tablename__ = 'Projects'
    projectid = db.Column('ProjectId', db.Integer, primary_key=True)
    userid = db.Column('UserId', db.Integer, db.ForeignKey('Users.Userid', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    projectname = db.Column('ProjectName', db.String(500), nullable=False)
    numberurls = db.Column('NumberUrls', db.Integer, nullable=False)
    uptime = db.Column('Uptime', db.Float, nullable=False)

