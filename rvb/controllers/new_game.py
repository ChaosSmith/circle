from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import NewGameForm

@application.route("/new_game", methods=["GET","POST"])
@login_required
def new_game():
    current_user = User.find(session["user_id"])
    form = NewGameForm()
    if request.method == 'POST' and form.validate_on_submit():
        Game.new_game(
            creator=current_user,
            name=form.name.data,
            height=form.height.data,
            length=form.length.data,
            villages=form.villages.data,
            password=form.password.data
            )
        return redirect(url_for("main"))
    elif request.method == 'POST':
        return render_template("new_game.html", user=current_user, form=form)
    elif request.method == 'GET':
        return render_template("new_game.html", user=current_user, form=form)
