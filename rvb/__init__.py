from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from rvb.db import parse_url, DATABASE

application = Flask(__name__)

application.config['SECRET_KEY'] = 'super-secret'
application.config['SQLALCHEMY_DATABASE_URI'] = parse_url(DATABASE)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


application.config['SECURITY_REGISTERABLE'] = True
application.config['SECURITY_CONFIRMABLE'] = False
application.config['SECURITY_REGISTER_URL'] = '/create_account'
application.config['SECURITY_PASSWORD_SALT'] = 'ReplaceThisSalt'

application.config['MAIL_SUPPRESS_SEND'] = True

db = SQLAlchemy(application)

from rvb.models import *

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(application, user_datastore)
mail = Mail(application)

from rvb.exceptions import *
from rvb.controllers import *

# Views
# @application.route('/')
# @login_required
# def home():
#     return 'Here you go!'



if __name__ == '__main__':
    application.run()
