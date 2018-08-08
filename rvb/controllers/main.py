from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError

@application.route("/", methods=["GET"])
@login_required
def main():
    current_user = User.find(session["user_id"])
    return render_template("main.html", user=current_user)
