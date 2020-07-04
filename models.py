import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String , nullable = False , unique= True )
    email = db.Column(db.String , nullable = False , unique = True )
    password = db. Column ( db.String , nullable = False)
    pid = db.relationship("Profile", backref="user" , lazy=True , uselist=False)


    def add_profile( self, bio , favGenre ):
        p = Profile(bio = bio , favGenre = favGenre , uid = self.id)
        db.session.add(p)
        db.session.commit()

    
class Profile(db.Model):
    __tablename__ ="profile"
    id = db.Column (db.Integer , primary_key = True)
    bio = db.Column (db.String , nullable = True)
    favGenre = db.Column (db.String , nullable = True)
    uid = db.Column (db.Integer ,db.ForeignKey("user.id") , nullable= False)
