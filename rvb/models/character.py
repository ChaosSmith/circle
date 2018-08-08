from rvb import db
from rvb.models import *
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError

class Character(db.Model, Base):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    game = db.relationship('Game', back_populates='characters')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    actions = db.Column(db.Integer)
    x = db.Column(db.Integer,nullable=False)
    y = db.Column(db.Integer,nullable=False)
    strength = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    experience = db.Column(db.Integer)
    max_health = db.Column(db.Integer)
    current_health = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Character %r>' % self.id

    def tick(self):
        self.update(actions=self.actions+1)

    def legal_moves(self):
        moves = [(self.x+1,self.y),(self.x-1,self.y),(self.x, self.y+1),(self.x,self.y-1)]
        return [move for move in moves if move[0] > -1 and move[0] <= self.game.length and move[1] > -1 and move[1] <= self.game.height]

    def move(self,x,y):
        if (x,y) in self.legal_moves():
            self.update(x=x,y=y)
