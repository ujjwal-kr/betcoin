from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect
from werkzeug.wrappers import request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    balance = db.Column(db.Integer,nullable=True, default=1000)


db.create_all()

@app.route("/")
def index():
    return render_template("bank.html")

@app.route("/add-account", methods=['GET', 'POST'])
def addAccount():
    if request.method == 'GET':
        return render_template("add-account.html")
    elif request.method == 'POST':
        try:
            wallet = Wallet(username=request.form.get("username"), 
            password=request.form.get("password"))
            db.session.add(wallet)
            db.session.commit()
            return redirect("/account")
        except:
            return "Try Again"