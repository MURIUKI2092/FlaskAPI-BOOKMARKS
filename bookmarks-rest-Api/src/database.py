from datetime import datetime
from lib2to3.pgen2.pgen import generate_grammar
from flask_sqlalchemy import SQLAlchemy #imported sqlAlchemy
import string
import random

database = SQLAlchemy() #initialised the SqlAlchemy

class User(database.Model): # created a model class for the User
    id = database.Column(database.Integer,primary_key=True)
    username=database.Column(database.String(80),unique=True,nullable=False)
    email=database.Column(database.String(120),unique=True,nullable=False)
    password=database.Column(database.Text(),nullable=False)
    created_at=database.Column(database.DateTime,default =datetime.now())
    updated_time = database.Column(database.DateTime,onupdate=datetime.now())
    bookmarks= database.relationship("Bookmark",backref='user') #created a relation with the Bookmark class model


    def __repr__(self) -> str:
        return 'User>>> {self.username}'

class Bookmark(database.Model): #created a bookmark Model
    id=database.Column(database.Integer,primary_key=True)
    body= database.Column(database.Text,nullable=True)
    url = database.Column(database.Text,nullable=False)
    short_url=database.Column(database.String(3),nullable=False)
    visits = database.Column(database.Integer,default=0)
    user_id=database.Column(database.Integer,database.ForeignKey("user.id")) # use the class relation identified by the User model
    created_at=database.Column(database.DateTime,default=datetime.now())
    updated_at = database.Column(database.DateTime,default=datetime.now())


    def generate_short_characters(self):
        characters= string.digits+string.ascii_letters # using the string imported obtain characters and digits from them
        picked_characters= ' '.join(random.choices(characters,k=3)) #the randomly picked list
        link = self.query.filter_by(short_url=picked_characters).first() #give a link if it exist from the db by 
        #carrying some queries and select the first one to appear

        if link: #check whether the link was found in the database
            self.generate_short_characters() #found keep selecting and redoing the queries until when it will not be found
        else:
            return picked_characters # if not found return the picked characters as the short characters

        pass

    
    
    def __init__(self,**kwargs): #override the cconstructor method for the app
        super().__init__(**kwargs)

        self.short_url= self.generate_short_characters()
    
    
    def __repr__(self) -> str:
        return 'BookMark >>>{self.url}'