from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError

@application.route("/", methods=["GET"])
def home():
    if "user_id" in session.keys():
        user = User.find(session["user_id"])
        return render_template("home.html", user=user, navbar=True)
    else:
        return render_template("home.html", user=None, navbar=False)
