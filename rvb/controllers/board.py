from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import JoinGameForm

@application.route("/board/<game_id>", methods=["GET"])
@login_required
def board(game_id):
    user = User.find(session["user_id"])
    game = Game.find(game_id)
    character = Character.find_by(game_id=game_id,user_id=session["user_id"])
    if game and character and game in user.games:
        open_encounter = Encounter.find_by(character_id=character.id, game_id=game_id, completed_at=None)
        if open_encounter: raise ApiError("Reload Required", 407)
        display = game.display(viewer=character)
        return render_template("board.html", game=game, display=display)
    else:
        raise ApiError("Action Not Permited", 400)
