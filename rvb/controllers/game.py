from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import JoinGameForm

@application.route("/game/<game_id>", methods=["GET","POST"])
@login_required
def game(game_id):
    user = User.find(session["user_id"])
    game = Game.find(game_id)
    if game:
        if game in user.games:
            # User is currently involved in this game
            display = game.display()
            return render_template("game.html", game=game, user=user, display=display)
        else:
            # User is not involved in this game, but should have the option to join in
            return redirect(url_for("join_game"))
    else:
        # Game does not exist
        return redirect(url_for("main"))
