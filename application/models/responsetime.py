from application.utils.extensions import db
from sqlalchemy_serializer import SerializerMixin

class Responsetime(db.Model, SerializerMixin):
    __tablename__ = 'ResponseTime'
    responseid = db.Column('ResponseId', db.Integer, primary_key=True)
    urlid = db.Column('UrlId', db.Integer, db.ForeignKey('Targets.UrlId', onupdate='CASCADE', ondelete='CASCADE'), index=True, nullable=False)
    timestamp = db.Column('Timestamp', db.DateTime)
    responsetime = db.Column('ResponseTime', db.Float)


