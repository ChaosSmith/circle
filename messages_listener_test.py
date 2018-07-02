import requests
from rvb import db
from rvb.models import *
from rvb.controls import *
import json

def test_get_listener(player, listener):
    host = "http://127.0.0.1:5000/"
    print("Can {player_name} get the listener?".format(player_name = player.name))
    params = {'api_key': player.api_key}
    response = requests.get(host + "listener/" + str(listener.id), params)
    print(response.text)

def test_post_listener(player, listener, channel):
    host = "http://127.0.0.1:5000/"
    if channel == "wrong_channel_id":
        print("Post to non existant channel as {player_name}".format(player_name=player.name))
        data = json.dumps({'channel_id': 9999999})
    elif channel:
        print("Can {player_name} post the listener?".format(player_name = player.name))
        print("Channel {channel_id}".format(channel_id=channel.id))
        data = json.dumps({'channel_id': channel.id})
    else:
        print("Post no channel_id as {player_name}".format(player_name=player.name))
        data = json.dumps({})

    params = {'api_key': player.api_key}
    response = requests.post(host + "listener/" + str(listener.id), params=params, data=data)
    print(response.text)

def test_post_message(player,channel,content):
    host = "http://127.0.0.1:5000/"
    print("Can {player_name} post the message to channel {channel_id}?".format(player_name = player.name, channel_id = channel.id))
    params = {'api_key': player.api_key}
    data = json.dumps({'content': content, 'channel_id': channel.id})
    response = requests.post(host + "messages", params=params, data=data)
    print(response.text)

def test_get_message(player, channel):
    host = "http://127.0.0.1:5000/"
    print("Can {player_name} get the message from channel {channel_id}?".format(player_name = player.name, channel_id = channel.id))
    params = {'api_key': player.api_key, 'channel_id': channel.id}
    response = requests.get(host + "messages", params)
    print(response.text)

new_game()

# lets build a little test for the interceptor

alpha = Player.query.filter(Player.name == 'Alpha').first()
bravo = Player.query.filter(Player.name == 'Bravo').first()
charlie = Player.query.filter(Player.name == 'Charlie').first()

listener = Listener.query.first()

channels = Channel.query.all()
channel_one = channels[0]
channel_two = channels[1]
channel_three = channels[2]

print("Can alpha post a message, and Bravo recieve it, but Charlie gets access denied?")
test_post_message(alpha,channel_one,"This is a test message! Did you get it?")
test_get_message(bravo,channel_one)
test_get_message(charlie,channel_one)

print("Bravo and alpha switch places")
test_post_message(bravo,channel_one,"This is a test message! Did you get it?")
test_get_message(alpha,channel_one)
test_get_message(charlie,channel_one)

print("No one should be able to read messages from other channels")
test_get_message(alpha,channel_two)
test_get_message(bravo,channel_two)
test_get_message(charlie,channel_two)
test_get_message(alpha,channel_three)
test_get_message(alpha,channel_three)
test_get_message(charlie,channel_three)

print("Can charlie get/post the listener between the channels?")
test_get_listener(charlie,listener)
test_post_listener(charlie,listener,channel_one)
test_get_listener(charlie,listener)
test_post_listener(charlie,listener,channel_two)
test_get_listener(charlie,listener)
test_post_listener(charlie,listener,channel_three)
test_get_listener(charlie,listener)
test_post_listener(charlie,listener,"wrong_channel_id")
test_get_listener(charlie,listener)
test_post_listener(charlie,listener,None)
test_get_listener(charlie,listener)

print("Lets make sure that all the other players get denied always!")
test_get_listener(alpha,listener)
test_post_listener(alpha,listener,channel_one)
test_get_listener(alpha,listener)
test_post_listener(alpha,listener,channel_two)
test_get_listener(alpha,listener)
test_post_listener(alpha,listener,channel_three)
test_get_listener(alpha,listener)
test_post_listener(alpha,listener,None)
test_get_listener(alpha,listener)
test_get_listener(bravo,listener)
test_post_listener(bravo,listener,channel_one)
test_get_listener(bravo,listener)
test_post_listener(bravo,listener,channel_two)
test_get_listener(bravo,listener)
test_post_listener(bravo,listener,channel_three)
test_get_listener(bravo,listener)
test_post_listener(bravo,listener,None)
test_get_listener(bravo,listener)

print("Now lets see if the intercepter can intercept")
test_post_listener(charlie,listener,channel_one)
test_post_message(alpha,channel_one,"This is a test message! Did you get it?")
test_get_listener(charlie,listener)

print("Lets see the decrypt over time")
for _ in range(10):
    test_post_message(alpha,channel_one,"This is a test message! Did you get it?")
test_get_listener(charlie,listener)




#Now that we have tested all of this, lets see about intercepting some messages
