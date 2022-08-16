from app import db
import datetime

# defines database schema for users and Messages


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(64))
    __table_args__ = {'extend_existing':True}


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    sender = db.Column(db.Integer)
    recipient = db.Column(db.Integer)
    content = db.Column(db.JSON)
    __table_args__ = {'extend_existing': True}
