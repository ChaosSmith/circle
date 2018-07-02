from rvb import db
from rvb.models import *
from datetime import datetime
import random
from sqlalchemy import func

class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    api_key = db.Column(db.String)
    ip_address = db.Column(db.String)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Message %r>' % self.id

    def create(name, description):
        new_player = Player(name=name, description=description)
        db.session.add(new_player)
        new_player.generate_api_key()
        db.session.commit()

    def find_or_assign(ip_address):
        player = Player.query.filter(Player.ip_address == ip_address).first()
        if player:
            return player
        else:
            players = Player.query.filter(Player.ip_address == None).all()
            if len(players) == 0:
                raise FullGame("Sorry this game is already full", 423)
            player = random.choice(players)
            player.ip_address = ip_address
            db.session.commit()
            return player

    def generate_api_key(self):
        self.api_key = '%030x' % random.randrange(16**30)

    def current_user(api_key):
        return Player.query.filter(Player.api_key == api_key).first()
