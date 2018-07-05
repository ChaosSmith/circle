import requests
from rvb import db
from rvb.models import *
from rvb.controls import *
import json

host = "http://127.0.0.1:5000/"
host = "http://10.88.111.49:8000/"

def test_get_agent(player, agent):
    if agent:
        print("Can {player_name} get the agent?".format(player_name = player.name))
        params = {'api_key': player.api_key, 'agent_id': agent.id}
        response = requests.get(host + "agent", params=params)
        print(response.text)
    else:
        print("Can {player_name} get all agents?".format(player_name = player.name))
        params = {'api_key': player.api_key}
        response = requests.get(host + "agent", params=params)
        print(response.text)

def test_post_agent(player, agent, x, y):
        print("Can {player_name} post the agent?".format(player_name = player.name))
        params = {'api_key': player.api_key, 'agent_id': agent.id}
        data = json.dumps({'x': x, 'y': y})
        response = requests.post(host + "agent", params=params, data=data)
        print(response.text)

new_game()

# lets build a little test for the interceptor

alpha = Player.query.filter(Player.name == 'Alpha').first()
bravo = Player.query.filter(Player.name == 'Bravo').first()
charlie = Player.query.filter(Player.name == 'Charlie').first()

agent = Agent.query.first()
package = Package.query.first()
safehouse = Package.query.first()

# Who knows what?

# Individual Agents
test_get_agent(alpha, agent)
test_get_agent(bravo, agent)
test_get_agent(charlie, agent)

# All Agents
test_get_agent(alpha, None)
test_get_agent(bravo, None)
test_get_agent(charlie, None)

# Who can move alpha's agent?
test_post_agent(alpha,agent,10,10) # Illegal Move

# Agent Runs around, grabs package, brings it to safe house
test_post_agent(alpha,agent,0,1)
test_post_agent(alpha,agent,0,2)
test_post_agent(alpha,agent,0,3)
test_post_agent(alpha,agent,0,4)
test_post_agent(alpha,agent,0,5)
test_post_agent(alpha,agent,0,6)
test_post_agent(alpha,agent,0,5)
test_post_agent(alpha,agent,0,4)
test_post_agent(alpha,agent,0,3)
test_post_agent(alpha,agent,0,2)
test_post_agent(alpha,agent,0,1)
test_post_agent(alpha,agent,0,0)
test_post_agent(alpha,agent,1,0)
test_post_agent(alpha,agent,2,0)
test_post_agent(alpha,agent,3,0)
test_post_agent(alpha,agent,4,0)
test_post_agent(alpha,agent,5,0)
test_post_agent(alpha,agent,6,0)
test_post_agent(alpha,agent,7,0)
test_post_agent(alpha,agent,8,0)
test_post_agent(alpha,agent,9,0)
test_post_agent(alpha,agent,10,0)
