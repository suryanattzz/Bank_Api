import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from bank_app.config import Config

app=Flask(__name__)
app.config.from_object(Config)
app.app_context().push()


db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'
login_manager.login_message_category='info'

mail=Mail(app)

from bank_app.users.routes import users
from bank_app.services.routes import services
from bank_app.main.routes import main
from bank_app.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(services)
app.register_blueprint(main)
app.register_blueprint(errors)