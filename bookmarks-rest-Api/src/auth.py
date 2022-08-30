from flask import Blueprint,request,jsonify
from werkzeug.security import check_password_hash,generate_password_hash
import validators
from src.database import User,database
auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")

@auth.post("/register")
def register():
    username = request.json['username'] # obtain the user name
    email=request.json['email'] #obtain the email
    password=request.json['password'] # obtain the password

    if len(password)<6: #check whether the user password is of required length
        return jsonify({"error":"password too short"}),400 # if not return this error

    if len(username)<3: #ccheck whether the username is of required length
        return jsonify({"error":"username too short"}),400 # if not return this error
    
    # if username.isalnum() or "  " in username: #checks whether the username is alphanumeric and no space is in the username
    #     return jsonify({"error":"username should be alphanumeric and also no spacecs"}),400 # if there is return the error

    if not validators.email(email): #check whether the email is valid
        return jsonify({"error":"Email is not valid"}),400 # If not valid return this

    #check whether the email exists in the database
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error":"The email is taken"}),409
#check whether the username is used by another person in the database
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error":"The username is taken"}),409

    hashed_password=generate_password_hash(password) # hash the user password
    user =User(username=username,password=hashed_password,email=email) #save the user's details together with the hashed password
    database.session.add(user) #add user to the database
    database.session.commit()#commit user to the database to update the changes which took place

    return jsonify({
        "message":"User created",
        'user':{
            'username':username,'email':email
        }
    }),201
    return "user registered"

@auth.get("/me")
def me():
    return {"user":"JAMES"}