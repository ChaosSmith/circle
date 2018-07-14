from rvb import application
from rvb.models import *
from flask import Flask, request, json
from rvb.controllers.helpers import authenticate, parse_data, validate_data
from rvb.exceptions import ApiError

@application.route('/agent', methods=['GET','POST'])
def agent():
    agent_id = request.args.get('agent_id')
    if request.method == 'POST':
        player = authenticate(request,['Charlie','Alpha'])
        if agent_id == None:
            raise ApiError("You must specify an agent!", 420)
        data = parse_data(request)
        validate_data(data,['x','y'])
        agent = Agent.find(int(agent_id))
        if agent.player != player:
            raise ApiError("You can't move someone elses agent!", 401)
        if agent:
            agent.move(int(data['x']),int(data['y']))
            if player.name == 'Alpha':
                return json.jsonify(
                    x=agent.x,
                    y=agent.y,
                    alive=agent.alive,
                    safehouse=agent.safehouse_id,
                    packages=len(agent.packages)
                )
            elif player.name == 'Charlie':
                return json.jsonify(
                    x=agent.x,
                    y=agent.y
                )
        else:
            raise ApiError("No agent found with id %r" % agent_id, 404)

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
                        alive=agent.alive,
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
                    raise ApiError('Access Denied', status_code=401)
            else:
                raise ApiError("No Agent found with id %r" % agent_id,404)

        else:
            if player.name == 'Alpha':
                return json.jsonify(agents=player.serialize_agents(player.name))
            elif player.name == 'Charlie':
                alpha = Player.query.filter(Player.name == 'Alpha').first()
                agents = player.serialize_agents('Charlie')
                agents.extend(alpha.serialize_agents('Charlie'))
                return json.jsonify(agents=agents)
            elif player.name == 'Bravo':
                charlie = Player.query.filter(Player.name == 'Charlie').first()
                return json.jsonify(agents=charlie.serialize_agents('Bravo'))
