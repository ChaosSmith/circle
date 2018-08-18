from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import CharacterCreationForm

@application.route("/create_character/<game_id>", methods=["GET","POST"])
@login_required
def create_character(game_id):
    character = Character.find_by(game_id=game_id,user_id=session["user_id"])
    if character: return redirect(url_for("game", game_id=game_id))
    user = User.find(session["user_id"])
    game = Game.find(game_id)
    form = CharacterCreationForm()
    if request.method == "POST" and form.validate_on_submit():
        character = Character.build(user, game, form)
        return redirect(url_for("game", game_id=game_id))
    elif request.method == "GET" or request.method == "POST":
        # Render Game Information And Button To Join, Possibly Game Password
        return render_template("create_character.html", user=user, form=form, game=game, navbar=True)
