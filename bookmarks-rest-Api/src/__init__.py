from flask import Flask,jsonify # import flask and jsonify
import os #import os to use the dot env key
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import database
from flask_jwt_extended import JWTManager


def create_app(test_config =None):
    app=Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),#obtain the secret key from the .env file
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),#obtain the database URI from the flask env
            SQLALCHEMY_TRACK_MODIFICATIONS=False, #  suppress the modifiation error generated by the Sql Alchemy.
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY')
        )
    else:
        app.config.from_mapping(test_config)
    database.app=app
    database.init_app(app) # control the integration of a pacckage to one or more Flask application
    JWTManager(app)#configure jwt so that when we call it can be known it's already there
    app.register_blueprint(auth) # register auth blueprint
    app.register_blueprint(bookmarks) #register bookmarks blueprint

    return app