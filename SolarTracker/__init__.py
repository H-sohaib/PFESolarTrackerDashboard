# from SolarTracker.authentication import routes
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pyrebase
from importlib import import_module
from .config import Config


firebaseConfig = {
    "apiKey": "AIzaSyAP60GlEBvuar_iAJCVqlJDapjfj8Tu_h8",
    "authDomain": "solartrackerpfe.firebaseapp.com",
    "databaseURL": "https://solartrackerpfe-default-rtdb.firebaseio.com/",
    "projectId": "solartrackerpfe",
    "storageBucket": "solartrackerpfe.appspot.com",
    "messagingSenderId": "162036465427",
    "appId": "1:162036465427:web:24e37f650928e7100364e6",
    "measurementId": "G-CWTXNSE2Z8"
}

# firebase
firebase = pyrebase.initialize_app(firebaseConfig)
firebaseDB = firebase.database()
# auth = firebase.auth()

login_manager = LoginManager()
db = SQLAlchemy()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    module_name = "authentication"
    module = import_module('SolarTracker.{}.routes'.format(module_name))
    app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app

app = create_app(Config)
# configure_database(app)
# module = import_module('SolarTracker.authentication.routes')
# app.register_blueprint(routes.blueprint)



