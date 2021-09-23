from app import app, db
from flask import render_template
from werkzeug.utils import redirect
from flask import request
from app.models import Wallet

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
            return redirect("/accounts")
        except:
            return "Try Again"

@app.route("/accounts")
def accounts_page():
    accounts = Wallet.query.all()
    return render_template("accounts.html", accounts=accounts)

@app.route("/accounts/<username>")
def getWallet(username):
    try:
        wallet = Wallet.query.filter_by(username=username).first()
        return render_template("wallet.html", wallet=wallet)
    except:
        return "User not found"    
            