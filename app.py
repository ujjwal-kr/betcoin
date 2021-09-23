from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from flask import request



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
db = SQLAlchemy(app)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer,nullable=True, default=1000)

def __init__(self, username):
   self.username = username

db.create_all()

@app.route("/")
def index():
    return render_template("bank.html")

@app.route("/signup", methods=['GET', 'POST'])
def addAccount():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        try:
            wallet = Wallet(username=request.form.get("username"), 
            password=request.form.get("password"))
            db.session.add(wallet)
            db.session.commit()
            return redirect("/account")
        except:
            return "Try Again"
            