from rvb import db
from rvb.models import *
from rvb.db import connect, drop, create, DATABASE

def new_game():
    clear_rows()

    Player.create(
        "Alpha",
        "You are on the blue team, codename Alpha. " + \
        "Your responsibility is to direct blue team agents to collect packages and take them to the required safehouse, " + \
        "while avoiding red team agents. " + \
        "Only you know the location of the pickups, communicate with blue team codename Bravo to find out the drop off locations, " + \
        "safehouses and the position of red team agents."
        )
    Player.create(
        "Bravo",
        "You are on the blue team, codename Bravo. " + \
        "Your responsibility is to keep track of red team agents and to communicate their movements to blue team codename Alpha, " + \
        "along with the location of his available dropoffs, and safehouses."
        )
    Player.create(
        "Charlie",
        "You are on the red team, codename Charlie. " + \
        "Your responsibility is to scan for blue team agents, while directing your own agents to intercept them. You can also attempt " + \
        "to listen in on blue team communications to discover the location of their safehouses, pickups, and dropoff locations."
        )

    Channel.create() #1
    Channel.create() #2
    Channel.create() #3

    Listener.create() #1

def clear_rows():
    Player.query.delete()
    Message.query.delete()
    Listener.query.delete()
    Channel.query.delete()

def recreate_db():
    engine = connect(None)
    drop(engine,DATABASE)
    create(engine,DATABASE)
    db.create_all()
