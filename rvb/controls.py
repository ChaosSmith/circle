from rvb import db
from rvb.models import *
from rvb.db import connect, drop, create, DATABASE

charlie = Player.query.filter(Player.name== 'Charlie').first()

def new_game():
    clear_rows()

def clear_rows():
    Agent.query.delete()
    Player.query.delete()

def recreate_db():
    engine = connect(None)
    drop(engine,DATABASE)
    create(engine,DATABASE)
    db.create_all()

def score():
    alpha = Player.query.filter(Player.name == 'Alpha')
    scored_packages = Package.query.filter(Package.safehouse_id != None).all()
    held_packages = Package.query.filter(Package.agent_id != None).all()
    unclaimed_packages = Package.query.filter(Package.agent_id == None and Package.safehouse_id == None).all()
    blue_agents_alive = Agent.query.filter(Agent.alive == True, Agent.player_id == alpha.id).all()
    blue_agents_dead = Agent.query.filter(Agent.alive == False, Agent.player_id == alpha.id).all()
    print("Scored Packages:", len(scored_packages))
    print("Held Packages:", len(held_packages))
    print("Unclaimed Packages:", len(unclaimed_packages))
    print("Blue Agents Alive:", len(blue_agents_alive))
    print("Blue Agents Dead:", len(blue_agents_dead))
