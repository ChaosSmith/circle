from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import JoinGameForm

@application.route("/encounter/<encounter_id>", methods=["GET","POST"])
@login_required
def encounter(encounter_id):
    user = User.find(session["user_id"])
    encounter = Encounter.find(encounter_id)
    game = encounter.game
    if game not in user.games: return redirect(url_for("home"))
    if encounter.finished(): return redirect(url_for("game", game_id=game.id))
    if request.method == "GET":
        return render_template(
            'encounter.html',
            game=game,
            user=user,
            encounter=encounter,
            scene=encounter.scenes[encounter.current_scene],
            navbar=True
        )
    if request.method == "POST":
        data = request.form.to_dict(flat=True)
        encounter.send(**data)
        if encounter.finished: return redirect(url_for("game", game_id=game.id))
        return render_template(
            'encounter.html',
            game=game,
            user=user,
            encounter=encounter,
            scene=encounter.scenes[encounter.current_scene],
            navbar=True
        )
