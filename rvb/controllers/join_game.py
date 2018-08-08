from rvb import application
from rvb.models import *
from flask import Flask, request, json, render_template, session, url_for, redirect
from flask_security import login_required
from rvb.controllers.helpers import parse_data, validate_data
from rvb.exceptions import ApiError
from rvb.forms import JoinGameForm

@application.route("/join_game", methods=["GET","POST"])
@login_required
def join_game():
    user = User.find(session["user_id"])
    form = JoinGameForm()
    if request.method == "POST" and form.validate_on_submit():
        game = Game.find(form.game_id.data)
        if game:
            # Game exists
            if game.password:
                # Game has a password
                if game.password == form.password.data:
                    user.join_game(game.id)
                    return redirect(url_for("main"))
                else:
                    form.password.errors.append("Password is incorrect")
                    return render_template("join_game.html", user=user, form=form)
            else:
                # No password clear to join
                # TODO enforce player limits in a game
                user.join_game(game.id)
                return redirect(url_for("main"))
        else:
            # Game Does Not Exists
            form.game_id.errors.append("Could not find a game with id #{id}".format(id=form.game_id.data))
            return render_template("join_game.html", user=user, form=form)

    elif request.method == "GET" or request.method == "POST":
        # Render Game Information And Button To Join, Possibly Game Password
        return render_template("join_game.html", user=user, form=form)
