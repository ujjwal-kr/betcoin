from app import db

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer,nullable=True, default=1000)
    inDept = db.Column(db.Integer, default=0)

class Bank(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, default=400000)

# class Transactions(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     sender = 


