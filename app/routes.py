import random
from app import app, db
from flask import render_template
from werkzeug.utils import redirect
from flask import request
from app.models import Wallet, Bank, Transactions

db.create_all()

@app.route("/")
def index():
    return render_template("bank.html")

@app.route("/signup", methods=['GET', 'POST'])
def addAccount():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        userform = str(request.form.get("username")).lower()
        if len(userform) < 2:
            return "Username cant be less than 2 characters" # Dont PR securuty issue cuz i know its a security issue and I'm just lazy
        bank = Bank.query.all()
        if len(bank) >= 1:
            try:
                if userform != "bank":
                    wallet = Wallet(username=userform, 
                    password=request.form.get("password"))
                    db.session.add(wallet)
                    db.session.commit()
                    return redirect("/accounts")
                else: return "Username cant be bank"   
            except:
                return "Try Again"
        else: 
            return "Ask the admin to create the bank"       

@app.route("/accounts")
def accounts_page():
    accounts = Wallet.query.order_by(Wallet.balance.desc()).all()
    if len(accounts) < 1: return "No Accounts created yet"
    return render_template("accounts.html", accounts=accounts)

@app.route("/accounts/<username>")
def getWallet(username):
    try:
        wallet = Wallet.query.filter_by(username=username).first()
        return render_template("wallet.html", wallet=wallet)
    except:
        return "User not found"


@app.route("/make/<passcode>")
def makeBank(passcode):
    existingBank = Bank.query.all()
    print(len(existingBank))
    if len(existingBank) == 1:
        return "Bank already created"
    else:
        if passcode == "makebank":
            bank = Bank()
            db.session.add(bank)
            db.session.commit()
            return redirect("/")
        else: return "Wrong password"

@app.route("/loan", methods=['POST'])
def takeLoan():
    wallet = Wallet.query.filter_by(username=request.form.get("username")).first()
    if request.form.get("password") == wallet.password:
        if int(request.form.get("loanValue")) > 5000:
            return "Cannot take loan more than 3000"
        elif int(request.form.get("loanValue")) < 500:
            return "Cannot take loan less than 500"
        if wallet.inDebt == 1:
            return "Already In Debt"       
        bank = Bank.query.get(1)
        bank.balance = bank.balance - int(request.form.get("loanValue"))
        wallet.inDebt = 1
        wallet.balance = wallet.balance + int(request.form.get("loanValue"))
        sender = "bank"
        reciever = wallet.username
        amount = int(request.form.get("loanValue"))
        transaction = Transactions(sender=sender, reciever=reciever, amount=amount)
        wallet.lastDebt = wallet.rounds
        wallet.debt = int(request.form.get("loanValue"))
        db.session.add(transaction)
        db.session.commit()
        return redirect("/accounts/" + wallet.username)     
    else: return "Wrong Password"  

@app.route("/send", methods=['POST'])
def send():
    try: 
        sender = Wallet.query.filter_by(username=request.form.get("username")).first()
        reciever = Wallet.query.filter_by(username=request.form.get("reciever")).first()
        amount = int(request.form.get("amount"))
        password = request.form.get("password")

        if password != sender.password:
            return "Incorrect Password"
        if amount < 1:
            return "Cant transfer empty coin"
        elif amount > 5000:
            return "Cant transfer coin more than 5000"
            
        if sender.balance < amount:
            return "You dont have enough money"
        else:
            sender.balance = sender.balance - amount
            reciever.balance = reciever.balance + amount
            transaction = Transactions(reciever=reciever.username, 
            sender=sender.username,
            amount=amount)
            db.session.add(transaction)
            db.session.commit()
            return redirect("/accounts/"+reciever.username)
    except: return "Try Again"

@app.route("/transactions", methods=['GET', 'POST'])
def transactions():
    if request.method == 'GET':
        return render_template("transactions.html")
    if request.method == 'POST':
        username = request.form.get("username")
        try: 
            wallet = Wallet.query.filter_by(username=username).first()
            return redirect("/transactions/"+username)
        except: return "User not found"

@app.route("/transactions/<username>", methods=["GET"])
def transaction(username):
    try:
        wallet = Wallet.query.filter_by(username=username).first()
        if len(wallet.username) < 1:
            return "User not found"
        sends = Transactions.query.filter_by(sender=username)
        recieves = Transactions.query.filter_by(reciever=username)
        return render_template("transaction.html", recieves=recieves, 
        sends=sends, 
        username=username)
    except: return "something went wrong"    

@app.route("/casino", methods=['GET', 'POST'])
def casino():
    if request.method == 'GET':
        return render_template("casino.html")
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")
        amount = request.form.get("amount")
        bank = Bank.query.get(1)
        try: 
            wallet = Wallet.query.filter_by(username=username).first()
            if password == wallet.password:
                if int(amount) > wallet.balance:
                    return "You dont have enough money"    
                if int(amount) > 100:
                    wallet.rounds = wallet.rounds + 1
                    if wallet.inDebt == 1:
                        if wallet.lastDebt + 7 == wallet.rounds:
                            wallet.balance = wallet.balance - wallet.debt
                            debtValue = wallet.debt
                            wallet.debt = 0
                            wallet.inDebt = 0
                            transaction = Transactions(sender=username, reciever="bank", amount=debtValue)
                            db.session.add(transaction)
                            db.session.commit()
                            return render_template("debtPay.html", balance=wallet.balance, debtValue=debtValue)
                    coin = random.randint(0,1)
                    if coin == 0:
                        wallet.balance = wallet.balance - int(amount)
                        bank.balance = bank.balance + int(amount)
                        wallet.wins = int(wallet.wins) - 1
                        transaction = Transactions(sender=username, reciever="bank", amount=amount)
                        db.session.add(transaction)
                        db.session.commit()
                        return render_template("results.html", resultText=username+" lost!", 
                        resultText2=username + " loses "+str(amount)+" in the gamble")
                    else:
                        percentage  = random.randint(1, 100)
                        amount = int(amount)
                        amount = amount + percentage/100 * amount
                        wallet.balance = wallet.balance + amount
                        bank.balance = bank.balance - amount
                        wallet.wins = int(wallet.wins) + 1
                        transaction = Transactions(sender="bank", reciever=username, amount=amount)
                        db.session.add(transaction)
                        db.session.commit()
                        return render_template("results.html", resultText=username+" wins!", 
                        resultText2=username + " wins "+str(amount)+" in the gamble with " + str(percentage)+"% increase")
                else: return "Cant bet for less than 100"       
            else: return "Wrong Password"
        except: return "User Not Found"    
