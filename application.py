import os

from flask import Flask, session 
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
#added myself 
from flask import render_template , url_for , redirect , request  , flash, jsonify
from flask_bootstrap import Bootstrap
import requests, json



app = Flask(__name__)
Bootstrap(app)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
# session maker generate a new session 
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
@app.route("/home")
def index():
    return "Project 1: TODO"

# Login : I need session, when the user login , will stay in that session so when they do a query , will not distrub the database
# login need to query my database so that I can 
@app.route("/login" , methods=["POST" ,"GET"])
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
            flash('User does not exists. Please register before login!!', 'error')
            return render_template("login.html" , buttonMsg ='Login') 
        # elif user.password is inputPassword:
        #     return render_template("login.html" , buttonMsg ='Login' , message=user.password) 
        else:
            flash('Already Login!!!' , 'message')
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
    if request.method == "POST":
        inputUsername = request.form["username"]
        inputEmail = request.form["email"]
        inputPassword = request.form["password"]

        # make sure no same username
        if db.execute("SELECT * FROM \"user\" WHERE username = :username AND email = :email AND password = :password " , 
                        {"username": inputUsername, "email": inputEmail , "password": inputPassword}).rowcount == 0 : 
            # add into database 
            db.execute("INSERT INTO \"user\" (username , email , password) VALUES (:username , :email , :password)" , 
                        {"username": inputUsername , "email": inputEmail , "password": inputPassword})
            db.commit()
            return render_template("profile.html" , username=inputUsername)
        else: 
            # flash message that this user already exist 
            flash('This user already exists!!! Try Again', 'error')
            return render_template("register.html" , buttonMsg ="Register" )
    else:
        return render_template("register.html" , buttonMsg ="Register")

@app.route("/profile")
def profile():
    # if there is a user in this session , i will redirect them back tp their profile page
    if "user" in session:
        user = session["user"]
        return render_template("profile.html" , username=user)
    else: 
    # if there the user is not in the session , i will redirect them to the login page 
    # this means that I havent login / i left my brower and I need to login again 
    # so i can redirect them to the login page
        return redirect(url_for("login"))
    
    return render_template("profile.html" , username=user)

# this is to remove the user 
@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    flash('Logout Successfully!' , 'message')
    session.pop("user" , None)
    return redirect(url_for("login"))



@app.route("/search",methods = ['GET', 'POST'])
def search():
    #when user click on the search button will start accesing the api 
    count = 0
    allResult = []
    if request.method == "POST":
        searchInput = request.form["search"]
        key="AIzaSyAlxOzntVoCg_q3MZc_pYgBeOSyuOLRp9o"
        res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={searchInput}&key={key}")
        #loop the raw data from google
        result = json.loads(res.text)
        if result is None:
            return abort(404)
        else: 
            for r in result['items']:
                if count < 10: 
                    count = count + 1 
                    try: 
                        # some of the data does not have an image and search info 
                        eachResult ={
                            "self_link" : r['selfLink'],
                            "title" : r['volumeInfo']['title'],
                            "authors" : r['volumeInfo']['authors'],
                            "categories" : r['volumeInfo']['categories'],
                            "avgRating" : r ['volumeInfo']['averageRating'],
                            "img" : r['volumeInfo']['imageLinks']['smallThumbnail'],
                            "description" : r['searchInfo']['textSnippet'], 
                        }
                        allResult.append(eachResult)
                        # return render_template("search.html" , results = r )
                    except KeyError:
                        pass 
                    #print(img)
            return render_template("search.html" , results =allResult)

    return render_template("search.html")
