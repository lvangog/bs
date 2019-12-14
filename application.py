import os
import random
import json

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, apology


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///scout.db")


@app.route("/runads", methods=["GET", "POST"])
def runads():
    if request.method == "GET":

        rows = db.execute("SELECT link FROM videos")

        # Create list of dict values from rows
        dict_list = []
        for row in rows:
            link = row['link']
            dict_list.append(link)

        # Select 10 random values from list and input into new list
        if len(dict_list) < 10:
            data = dict_list

        else:
            data = random.sample(dict_list, 10)

        # Put each list element into json format
        # For some reason there was an issue and I couldn't access
        # the list elements if I performed json.dumps on
        # the entire list, so I had to do each entry
        data1 = json.dumps(data[0])
        data2 = json.dumps(data[1])
        data3 = json.dumps(data[2])
        data4 = json.dumps(data[3])
        data5 = json.dumps(data[4])
        data6 = json.dumps(data[5])
        data7 = json.dumps(data[6])
        data8 = json.dumps(data[7])
        data9 = json.dumps(data[8])
        data10 = json.dumps(data[9])


        # Pass list elements to template
        return render_template("runads.html",
        data1 = data1, data2 = data2, data3 = data3, data4 = data4, data5 = data5,
        data6 = data6, data7 = data7, data8 = data8, data9 = data9, data10 = data10)



@app.route("/upload", methods=["GET", "POST"])
def upload():

    # Get
    if request.method == "GET":
        return render_template("upload.html")
    # Post
    else:
        if not request.form.get("upload"):
            return apology("Must provide video URL")

        url = request.form.get("upload")

        # Make sure url is in the correct format
        if url.find("https://www.youtube.com/embed/") == -1:
            return apology("Invalid URL. See example")

        # Insert into SQL database
        db.execute("INSERT INTO videos (link, id) VALUES (:link, :id)", link = url, id = session["user_id"])
        return render_template("index.html")


@app.route("/team", methods=["GET"])
def team():
    return render_template("team.html")



@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



@app.route("/user_account", methods=["GET"])
def user_account():
    return render_template("user_account.html")



@app.route("/advertiser_account", methods=["GET"])
def advertiser_account():
    return render_template("advertiser_account.html")



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
        rows = db.execute("SELECT * FROM accounts WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember whether user is an advertiser or not
        session["user_id"] = rows[0]["id"]
        if rows[0]['advertiser'] == "TRUE":
            session["admin"] = True
        else:
            session["admin"] = False

        print(rows[0]['advertiser'])


        return redirect('/')

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




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Get
    if request.method == "GET":
        print("")
        return render_template("register.html")

    # Post
    else:
        print("tst")
        # Check if username was submitted
        if not request.form.get("username"):
            return apology("must input username", 403)

        # Check if password was submitted
        elif not request.form.get("password"):
            return apology("must input password", 403)


        password = request.form.get("password")
        username = request.form.get("username")

        # Generate hash for password
        passwordHash = generate_password_hash(password, method ='pbkdf2:sha256', salt_length = 8)

        advertiser = False
        # Insert into accounts table
        if not request.form.get("checkbox"):
            submission = db.execute("INSERT INTO accounts (username, hash, advertiser) VALUES (:username, :hash, :advertiser)", username = username, hash = passwordHash, advertiser= 'FALSE')

        else:
            submission = db.execute("INSERT INTO accounts (username, hash, advertiser) VALUES (:username, :hash, :advertiser)", username = username, hash = passwordHash, advertiser= 'TRUE')
            advertiser = True
        # Check if username is taken
        if not submission:
            return apology("invalid submission", 403)

        # Use session to remember user (advertiser or not)
        session["user_id"] = submission
        if advertiser:
            session["admin"] = True
        else:
            session["admin"] = False
        print(session)
        # Direct to homepage
        return redirect("/")

