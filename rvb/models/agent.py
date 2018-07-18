from rvb import db
from rvb.db.base import Base
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError
from rvb.models.player import Player

class Agent(db.Model, Base):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    player = db.relationship('Player', back_populates='agents')
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False, index=True)
    x = db.Column(db.Integer,nullable=False, index=True)
    y = db.Column(db.Integer,nullable=False, index=True)
    tagged = db.Column(db.Boolean, server_default='f', nullable=False)
    created_at =db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at =db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Agent %r>' % self.id
    
    def tag(self):
        self.update(tagged=True)

    def legal_moves(self):
        moves = [(self.x+1,self.y),(self.x-1,self.y),(self.x, self.y+1),(self.x,self.y-1)]
        return [move for move in moves if move[0] > -1 and move[0] < 100 and move[1] > -1 and move[1] < 100]

    def serialize(self, requestor):
        return {'id': self.id, 'tagged': self.tagged, 'owner': self.player.name, 'x': self.x, 'y': self.y}

    def move(self,x,y):
        if (x,y) not in self.legal_moves():
            raise ApiError(
                "Agent {agent_id} can't move to {x},{y}, only to [{legal_moves}]".format(
                    agent_id=self.id,
                    x=x,
                    y=y,
                    legal_moves=",".join([str(move) for move in self.legal_moves()])
                    ),
                404
                )
        self.update(x=x,y=y)

        if self.tagged:
            tags = []
            for agent in Agent.where(x=x,y=y,tagged=False):
                agent.tag()
                tags.append(agent.player.name)
            if len(tags) > 0:
                return "Moved to ({x},{y}) and tagged [{players}]".format(players=",".join(tags),x=x,y=y)
            else:
                return "Moved to ({x},{y})".format(x=x,y=y)
        else:
            agent = Agent.find_by(x=x,y=y,tagged=True)
            if agent:
                self.tag()
                return "Moved to ({x},{y}) and was tagged by {player}".format(player=agent.player.name, x=x,y=y)
            else:
                return "Moved to ({x},{y})".format(x=x,y=y)
