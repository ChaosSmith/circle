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
    character = Character.find_by(game_id=game_id,user_id=session["user_id"])
    if game:
        if game in user.games:
            # User is currently involved in this game
            if character:
                # Already Has Character
                display = game.display(viewer=character)
                return render_template("game.html", game=game, user=user, display=display, navbar=True)
            else:
                # No Character Yet
                return redirect(url_for("create_character",game_id=game.id))
        else:
            # User is not involved in this game, but should have the option to join in
            return redirect(url_for("join_game"))
    else:
        # Game does not exist
        return redirect(url_for("home"))
