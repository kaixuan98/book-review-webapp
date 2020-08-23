import os
from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#added myself 
from flask import render_template , url_for , redirect , request , flash
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
    # if someone is filling in the form need to check with the data base
    # if it in the database then i need to redirected them to their session 
    message=''
    if request.method == "POST":
        inputEmail = request.form["email"]
        inputPassword = request.form["password"]
        # need to do a validation if that user in my database 
        user = db.execute("SELECT * FROM \"user\" WHERE email = :email AND password = :password" ,{"email": inputEmail , "password" : inputPassword} ).fetchone()
        if user is None:
            flash("User does not exists. Please register before login!!", 'error')
            return render_template("login.html" , buttonMsg ='Login') 
        # elif user.password is inputPassword:
        #     return render_template("login.html" , buttonMsg ='Login' , message=user.password) 
        else:
            #flash("Login Successfully", 'message')
            session["user"] = user.username
            return redirect(url_for('profile'))
            
    else: 
        # if the user already in the session ( already login ) we can redirect them back to their profile page
        if "user" in session:
            return redirect(url_for("profile"))  
                
        return render_template("login.html" , buttonMsg ='Login')

# Register: I need to take in the username , email and password and save it into my database 
# How can i pass those variable into the database??
# making sure their username and password is unqiue then I can redirect them to their profile page 
# if they are repeated username = need to flash message that say it is a repeated message ( flash messages)


@app.route("/register" , methods=["GET","POST"])
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
            flash("Succesfully created an account !!!! ", 'message')
            return render_template("profile.html" , username=inputUsername)
        else: 
            # flash message that this user already exist 
            flash("This user already exists!!! Try Again" , 'error')
            return render_template("register.html" , buttonMsg ="Register")
    else:
        return render_template("register.html" , buttonMsg ="Register")

    return render_template('register.html',buttonMessage=buttonMessage)

@app.route("/home", methods=['POST'])
def home():
    if "user" in session:
        user = session["user"]
        return f"<h1>{user}</h1>"
    else:
        return redirect(url_for('login'))

# this is to remove the user 
@app.route("/logout")
def logout():
    session.pop("user" , None)
    flash("Logout Successfully !!! " , 'message')
    return redirect(url_for("login"))


@app.route("/search")
def search():
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)