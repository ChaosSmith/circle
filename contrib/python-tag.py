import argparse
import glob
import hashlib
import json
import requests
import random

url='http://10.88.111.181:8000/'

def req(action, method='get', params={}, data={}):
	response=requests.request(method, url+action, params=params, data=json.dumps(data))
	try: return response.json()
	except: pass

def rename_player(player, name):
	req('player', 'post', {'api_key': player['api_key']}, {'name': name})

def create_player():
	player=req('player')
	name=hashlib.sha256(player['api_key'].encode()).hexdigest()
	with open('player_{}.txt'.format(name), 'w') as file:
		file.write(json.dumps(player))
	rename_player(player, name)
	print('created player with name '+name)

def get_player(name):
	file_name=glob.glob('player_{}*.txt'.format(name))[0]
	with open(file_name) as file: contents=file.read()
	return json.loads(contents)

def get_player_location(name):
	response=req('agent')
	for player in response['agents']:
		if player['owner'].startswith(name):
			return (player['x'], player['y'])

def move_player(name, direction):
	player=get_player(name)
	x, y=get_player_location(name)
	dx, dy={
		'right': (1, 0),
		'left': (-1, 0),
		'up': (0, 1),
		'down': (0, -1),
	}[direction]
	x+=dx
	y+=dy
	req('agent', 'post', {'api_key': player['api_key']}, {'x': x, 'y': y})

parser=argparse.ArgumentParser()
parser.add_argument('--create', action='store_true')
parser.add_argument('--name')
parser.add_argument('--move')
parser.add_argument('--flee', action='store_true')
parser.add_argument('--chase', action='store_true')
args=parser.parse_args()

if args.create: create_player()

if args.move:
	move_player(args.name, args.move)

class Vector:
	def __init__(self, x=0, y=0):
		self.x=x
		self.y=y
	def __add__(self, other):
		return Vector(self.x+other.x, self.y+other.y)
	def __sub__(self, other):
		return Vector(self.x-other.x, self.y-other.y)
	def div(self, scalar):
		return Vector(self.x/scalar, self.y/scalar)
	def d2(self):
		return self.x**2+self.y**2

def flee():
	while True:
		response=req('agent')
		baddies=[]
		for player in response['agents']:
			if player['owner'].startswith(args.name):
				me=Vector(player['x'], player['y'])
			elif player['tagged']:
				baddies.append(Vector(player['x'], player['y']))
		force=Vector()
		for baddie in baddies:
			force+=(me-baddie).div((me-baddie).d2())
		if force.x>0 and me.x==99: force.x=0
		if force.x<0 and me.x== 0: force.x=0
		if force.y>0 and me.y==99: force.y=0
		if force.y<0 and me.y== 0: force.y=0
		if (force.x==0 and force.y==0) or random.random()<0.2:
			force.x=random.random()-0.5
			force.y=random.random()-0.5
		for i in range(4):
			if abs(force.x)>abs(force.y):
				if force.x>0:
					move_player(args.name, 'right')
				else:
					move_player(args.name, 'left')
			else:
				if force.y>0:
					move_player(args.name, 'up')
				else:
					move_player(args.name, 'down')

if args.flee: flee()

def chase():
	while True:
		response=req('agent')
		victims=[]
		for player in response['agents']:
			if player['owner'].startswith(args.name):
				me=Vector(player['x'], player['y'])
			elif not player['tagged']:
				victims.append(Vector(player['x'], player['y']))
		closest=Vector(1000, 1000)
		for victim in victims:
			if (me-victim).d2()<(me-closest).d2():
				closest=victim
		force=closest-me
		if force.x>0 and me.x==99: force.x=0
		if force.x<0 and me.x== 0: force.x=0
		if force.y>0 and me.y==99: force.y=0
		if force.y<0 and me.y== 0: force.y=0
		if abs(force.x)>abs(force.y):
			if force.x>0:
				move_player(args.name, 'right')
			else:
				move_player(args.name, 'left')
		else:
			if force.y>0:
				move_player(args.name, 'up')
			else:
				move_player(args.name, 'down')

if args.chase: chase()
