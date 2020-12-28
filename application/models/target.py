from application.utils.extensions import db
from sqlalchemy_serializer import SerializerMixin

class Target(db.Model, SerializerMixin):
    __tablename__ = 'Targets'
    urlid = db.Column('UrlId', db.Integer, primary_key=True)
    projectid = db.Column('ProjectId', db.Integer, db.ForeignKey('Projects.ProjectId', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    link = db.Column('Link', db.String(2000))
    testtype = db.Column('TestType', db.String(500), nullable=False)
    numsuccess = db.Column('NumSuccess', db.Integer, nullable=True)
    numfailure = db.Column('NumFailure', db.Integer, nullable=True)
    mostrecentstatus = db.Column('MostRecentStatus', db.String(100), nullable=True)
    mostrecenterror = db.Column('MostRecentError', db.String(2000), nullable=True)
    requestheaders = db.Column('RequestHeaders', db.String(3000), nullable=True)
    requestbody = db.Column('RequestBody', db.String(3000), nullable=True)
    requesttype = db.Column('RequestType', db.String(100), nullable=True)


