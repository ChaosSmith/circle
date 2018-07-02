from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy
from rvb.db import parse_url, DATABASE

application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = parse_url(DATABASE)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

from rvb.models import *
from rvb.exceptions import *
from rvb.controllers import *

@application.route('/')
def hello():
    return "Hello :)! You have found the rvb api!"

# @application.route('/game', methods=['GET', 'POST'])
# def game():
#     if request.method == 'POST':
#         pass
#     elif request.method == 'GET':
#         pass
