import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    """Show portfolio of stocks"""
    id = session.get("user_id")
    lines = db.execute("SELECT symbol, shares FROM stocks WHERE user_id = ?", id)
    cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
    cash = cash[0]["cash"]
    total = cash

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("cash"):
            return apology("must provide valid number", 403)
        else:
            db.execute("UPDATE users SET cash = ? WHERE id = ?",
                       cash + float(request.form.get("cash")), id)
            return redirect("/")

    elif lines:
        for line in lines:
            price_info = lookup(line["symbol"])
            line["price"] = price_info["price"]
            total = total + line["price"] * line["shares"]

        return render_template("index.html", cash=cash, rows=lines, line=line, total=total)
    else:
        return render_template("index.html", cash=cash, rows=lines, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol") or lookup(request.form.get("symbol")) == None:
            return apology("must provide valid symbol", 400)

        # Ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide a valid share number", 400)
        else:
            try:
                shares = float(request.form.get("shares"))
            except ValueError:
                return apology("shares must be a number", 400)

        if not shares.is_integer() or shares <= 0:
            return apology("must provide a valid share number", 400)

        else:
            try:
                symbol = lookup(request.form.get("symbol"))
                share_number = request.form.get("shares")
                id = session.get("user_id")

                stock_price = float(symbol["price"]) * float(share_number)
                cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
                cash = cash[0]["cash"]

                if stock_price > cash:
                    apology("You dont have enough cash", 403)
                else:
                    rows_updated = db.execute(
                        "UPDATE stocks SET shares = shares + ? WHERE symbol = ? AND user_id = ?", share_number, symbol["symbol"], id)
                    if rows_updated == 0:
                        db.execute("INSERT INTO stocks (user_id, symbol, shares) VALUES(?, ?, ?)",
                                   id, symbol["symbol"], share_number)

                    # log of the buy
                    db.execute("INSERT INTO logs (user_id, symbol, shares) VALUES(?, ?, ?)",
                               id, symbol["symbol"], share_number)

                    db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - stock_price, id)
                    return redirect("/")
            except (KeyError, IndexError, requests.RequestException, ValueError):
                return None

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id = session.get("user_id")
    lines = db.execute(
        "SELECT symbol, shares, time FROM logs WHERE user_id = ? ORDER BY time ASC", id)

    if lines:
        for line in lines:
            price_info = lookup(line["symbol"])
            line["price"] = price_info["price"]

        return render_template("history.html", rows=lines, line=line)
    else:
        return render_template("history.html", rows=lines)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must provide valid symbol", 400)
        else:
            symbol = request.form.get("symbol")
            if lookup(symbol) == None:
                return apology("That Symbol does not exist")
            else:
                symbol = lookup(symbol)
                return render_template("quote.html", symbol=symbol)

    return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username was submitted
        if not request.form.get("username") or len(rows) != 0:
            return apology("must provide valid username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not request.form.get("confirmation") or request.form.get("confirmation") != request.form.get("password"):
            return apology("must provide valid confirmation", 400)

        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?);", request.form.get(
                "username"), generate_password_hash(request.form.get("confirmation")))

            return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    id = session.get("user_id")
    options = db.execute("SELECT symbol FROM stocks WHERE user_id = ? GROUP BY symbol", id)
    get_shares = request.form.get("shares")

    cash = db.execute("SELECT cash FROM users WHERE id = ?", id)
    cash = cash[0]["cash"]

    enf_chares = db.execute(
        "SELECT shares FROM stocks WHERE user_id = ? AND symbol = ? GROUP BY symbol", id, request.form.get("symbol"))

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("must chose an option", 403)
        elif not get_shares or float(get_shares) > float(enf_chares[0]["shares"]):
            return apology("must chose valid quantity of shares", 400)

        symbol = lookup(request.form.get("symbol"))

        stock_price = float(symbol["price"]) * float(get_shares)

        db.execute("UPDATE stocks SET shares = ? WHERE user_id = ? AND symbol = ?", float(
            enf_chares[0]["shares"]) - float(get_shares), id, request.form.get("symbol"))
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + stock_price, id)

        # log of sell
        db.execute("INSERT INTO logs (user_id, symbol, shares) VALUES(?, ?, ?)",
                   id, symbol["symbol"], float(get_shares) * -1)
        return redirect("/")

    return render_template("sell.html", options=options)
