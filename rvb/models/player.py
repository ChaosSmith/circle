from rvb import db
from rvb.models import *
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    agents = db.relationship('Agent', back_populates='player')
    description = db.Column(db.Text)
    api_key = db.Column(db.String)
    ip_address = db.Column(db.String)
    team = db.Column(db.String)
    permissions = db.Column(db.JSON, server_default='[]', nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Player %r>' % self.id

    def create(name, description):
        new_player = Player(name=name, description=description)
        db.session.add(new_player)
        new_player.generate_api_key()
        db.session.commit()
        return new_player

    def find_or_assign(ip_address):
        player = Player.query.filter(Player.ip_address == ip_address).first()
        if player:
            return player
        else:
            players = Player.query.filter(Player.ip_address == None).all()
            if len(players) == 0:
                raise ApiError("Sorry this game is already full", 423)
            player = random.choice(players)
            player.ip_address = ip_address
            db.session.commit()
            return player

    def current_user(api_key):
        return Player.query.filter(Player.api_key == api_key).first()

    def generate_api_key(self):
        self.api_key = '%030x' % random.randrange(16**30)

    def serialize_agents(self,requestor):
        if (requestor == 'Alpha' or requestor == 'Charlie') and self.name == 'Alpha':
            return [agent.serialize(requestor) for agent in self.agents if requestor == 'Alpha' or (not agent.in_safehouse() and requestor == 'Charlie')]
        elif (requestor == 'Charlie' or requestor == 'Bravo') and self.name == 'Charlie':
            return [agent.serialize(requestor) for agent in self.agents]
        else:
            raise ApiError("You are not permitted to access this resource!", 401)
