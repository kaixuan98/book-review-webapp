import os
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import render_template , request ,url_for , redirect
from flask_bootstrap import Bootstrap
from models import * 
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.secret_key = "thisisasecretKey"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route("/login" , methods=["GET" ,"POST"]) 
def login():
    # if request.method == "POST":
    #     user = request.form["username"]
    #     session['user'] = user 
    #     return redirect(url_for("home"))
    # else:
    
    buttonMessage = "Login" # since it is a inherited form so i need to rename the button 
    return render_template('login.html', buttonMessage = buttonMessage)

@app.route("/register" , methods=['GET' , 'POST'])
def register():
    buttonMessage = "Register"
    
    #get info from the form
    if request.method =='POST':
        try:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            user = User(username = username , email= email , password=password)
            db.add(user)
            db.commit()
        except IntegrityError:
            db.rollback()
            errorMsg = "This user already created an account !!! "
            return render_template('register.html',buttonMessage=buttonMessage , errorMsg=errorMsg)
        #user.add_profile(bio , favGenre)

    return render_template('register.html',buttonMessage=buttonMessage)

@app.route("/home", methods=['POST'])
def home():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for('login'))


@app.route("/profile" , methods=['POST'])
def profile():
    return render_template('profile.html')


@app.route("/search")
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)