from rvb import db
from rvb.models import *
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError
from rvb.models.agent import Agent

class Player(db.Model, Base):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    agents = db.relationship('Agent', back_populates='player')
    description = db.Column(db.Text)
    api_key = db.Column(db.String)
    ip_address = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Player %r>' % self.id

    def find_or_assign(ip_address):
        player = Player.find_by(ip_address=ip_address)
        if player:
            return player
        else:
            description = "Its a game of tag, try to be the last one standing!"
            api_key = '%030x' % random.randrange(16**30)
            player = Player.create(name="Noob", ip_address=ip_address, api_key=api_key, description=description)
            if Agent.size() == 0:
                agent = Agent.create(x=random.randint(1,99),y=random.randint(1,99), player_id=player.id, tagged=True)
            else:
                agent = Agent.create(x=random.randint(1,99),y=random.randint(1,99), player_id=player.id, tagged=False)

            return player

    def current_user(api_key):
        return Player.find_by(api_key=api_key)
