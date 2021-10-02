from datetime import timezone
from app import db
from sqlalchemy.sql import func

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer,nullable=True, default=1000)
    inDebt = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)
    rounds = db.Column(db.Integer, default=0)
    lastDebt = db.Column(db.Integer, default=0)
    debt = db.Column(db.Integer, default=0)

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, default=400000)

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String, nullable=False)
    reciever = db.Column(db.String, nullable=False)
    dateTime = db.Column(db.DateTime, default=func.now())
    amount =  db.Column(db.Integer,nullable=True)



