from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data

@application.route('/player', methods=['GET'])
def player():
    # If the ip has not been seen, assign a player randomly, along with the api key
    player = Player.find_or_assign(request.remote_addr)
    return json.jsonify(
        name=player.name,
        description=player.description,
        api_key=player.api_key
        )
