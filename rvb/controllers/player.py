from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data

@application.route('/player', methods=['GET', 'POST'])
def player():
    # If the ip has not been seen, assign a player randomly, along with the api key
    if request.method == 'POST':
        player = authenticate(request)
        data = parse_data(request)
        validate_data(data,['name'])
        player.update(name=data['name'])
        return "Your name is now {name}".format(name=data['name'])

    elif request.method == 'GET':
        player = Player.find_or_assign(request.remote_addr)
        return json.jsonify(
            name=player.name,
            description=player.description,
            api_key=player.api_key,
            agent_id=player.agents[0].id
            )
