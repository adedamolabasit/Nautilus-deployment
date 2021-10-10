from enum import unique
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import jsonify
from sqlalchemy.orm import backref


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:Nautilus5he!@localhost:5432/nautilus'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    Migrate(app,db)


class User(db.Model):
    __tablebame__='user'
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(23),nullable=False,unique=True)
    first_name=db.Column(db.String(),nullable=True)
    last_name=db.Column(db.String(),nullable=True)
    newsletter=db.relationship('NewsLetter',backref='owner',cascade='all,delete',lazy=True)

 



    def __repr__(self):
        return f'{self.first_name}'

    def __init__(self,username,first_name,last_name):
        self.username=username
        self.first_name=first_name
        self.last_name=last_name

    def format(self):
        return {
            'id':self.id,
            'username':self.username,
            'first name':self.first_name,
            'last name':self.last_name,
            
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()



class NewsLetter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    description=db.Column(db.Text,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def __init__(self,description):
        self.description=description

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "newsletter_details":
            {
                "newsletter id":self.id,
                "description":self.description,
                'created':self.user_id
            }
        }

    

    
    


  