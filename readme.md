# <code>BETCOIN</code>

Run on repl: https://repl.it/github/ujjwal-kr/betcoin

BET is a digital currency created with python and flask with features of a centralized  bank, wallet system, and open transaction history of all the users in the network including one to one deposit. It also has a betting (gambling) system and some other games will be added in future.

## How to run it

1. Download python
2. clone this repo: `git clone https://github.com/ujjwal-kr/betcoin.git`
3. run `python3 -m venv venv` for UNIX and `py -3 -m venv venv` for windows.
4. run `. venv/bin/activate` for UNIX and `venv\Scripts\activate` for windows.
5. run `pip install flask`
6. run `pip install flask_sqlalchemy`
7. run `export FLASK_ENV=development` for UNIX and `set FLASK_ENV=development` for windows (CMD) `$env:FLASK_ENV = "development"` (PowerShell) to enter debug mode.
8. run `flask run`
