from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.exceptions import ResourceMissing, InvalidUsage

@application.route('/agent/<agent_id>', methods=['GET','POST'])
def agent(agent_id):
    if request.method == 'POST':
        player = authenticate(request,['Charlie','Alpha'])
        if agent_id == None:
            raise InvalidUsage("You must specify an agent!", 420)
        data = parse_data(request)
        validate_data(data,['x','y'])
        agent = Agent.find(int(agent_id))
        if agent:
            agent.move(int(data['x']),int(data['y']))
            return "Agent moved to {x},{y}".format(x=data['x'],y=data['y'])
        else:
            raise ResourceMissing("No agent found with id %r" % agent_id, 404)

    elif request.method == 'GET':
        player = authenticate(request,['Alpha','Bravo','Charlie'])

        if agent_id:
            agent = Agent.find(agent_id)

            if agent:
                if player.name == 'Alpha' and agent.player.name == 'Alpha':
                    return json.jsonify(
                        id=agent.id,
                        x=agent.x,
                        y=agent.y,
                        safehouse=agent.safehouse_id,
                        packages=len(agent.packages)
                        )
                elif (player.name == 'Charlie' or player.name == 'Bravo') and agent.player.name == 'Charlie':
                    return json.jsonify(
                        id=agent.id,
                        x=agent.x,
                        y=agent.y
                        )
                elif player.name == 'Charlie' and not agent.in_safehouse() and agent.player.name == 'Alpha':
                    return json.jsonify(
                        id=agent.id,
                        x=agent.x,
                        y=agent.y,
                        packages=len(agent.packages),
                        )
            else:
                raise ResourceMissing("No Agent found with id %r" % agent_id,404)

        else:
            if player.name == 'Alpha':
                return player.serialize_agents(player.name)
            elif player.name == 'Charlie':
                alpha = Player.query.filter(Player.name == 'Alpha').first()
                return player.serialize_agents.extend(alpha.serialize_agents('Charlie'))
            elif player.name == 'Bravo':
                charlie = Player.query.filter(Player.name == 'Charlie').first()
                return charlie.serialize_agents('Bravo')
