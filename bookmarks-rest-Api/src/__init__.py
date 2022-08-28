from flask import Flask,jsonify # import flask and jsonify
import os #import os to use the dot env key

def create_app(test_config =None):
    app=Flask(__name__,instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY")#obtain the secret key from the .env file
        )
    else:
        app.config.from_mapping(test_config)
 
    @app.get("/")
    def index():
        return jsonify({"message":"Hello World"})

    return app