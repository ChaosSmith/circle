from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.exceptions import ApiError

@application.route('/agent', methods=['GET','POST'])
def agent():
    if request.method == 'POST':
        player = authenticate(request)
        data = parse_data(request)
        validate_data(data,['x','y'])
        agent = player.agents[0] # Player should only have one agent!
        message = agent.move(int(data['x']),int(data['y']))
        return json.jsonify(
            x=agent.x,
            y=agent.y,
            tagged=agent.tagged,
            message=message
        )

    elif request.method == 'GET':
        return json.jsonify(
            'agents'=[agent.serialize() for agent in Agent.all()]
            )
