from flask import Flask,jsonify # import flask and jsonify
import os #import os to use the dot env key
from src.auth import auth
from src.bookmarks import bookmarks
from src.database import database
def create_app(test_config =None):
    app=Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),#obtain the secret key from the .env file
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DATABASE_URI"),#obtain the database URI from the flask env
        )
    else:
        app.config.from_mapping(test_config)
    database.app=app
    database.init_app(app) # control the integration of a pacckage to one or more Flask application
    app.register_blueprint(auth) # register auth blueprint
    app.register_blueprint(bookmarks) #register bookmarks blueprint

    return app