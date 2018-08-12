from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import JoinGameForm

@application.route("/move", methods=["POST"])
@login_required
def move():
    data = request.form
    game_id = data["game_id"]
    user = User.find(session["user_id"])
    game = Game.find(game_id)
    character = Character.find_by(game_id=game_id,user_id=session["user_id"])
    if game and character and game in user.games:
        character.move(int(data['x']),int(data['y']))
        display = game.display(viewer=character)
        return render_template("board.html", game=game, display=display)
    else:
        raise ApiError("Action Not Permited", 400)
