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

def test_get_safehouses(player):
        print("Can {player_name} get the safehouses?".format(player_name = player.name))
        params = {'api_key': player.api_key}
        response = requests.get(host + "safehouses", params=params)
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
test_get_safehouses(alpha)
test_get_safehouses(bravo)
test_get_safehouses(charlie)
