from rvb import db
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ResourceMissing, IsDead, IllegalMove
from rvb.models import *
from rvb.models.safehouse import Safehouse
from rvb.models.package import Package
class Agent(db.Model):
    __tablename__ = 'agents'

    id = db.Column(db.Integer, primary_key=True)
    player = db.relationship('Player', back_populates='agents')
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False, index=True)
    safehouse = db.relationship('Safehouse', back_populates='agents')
    safehouse_id = db.Column(db.Integer, db.ForeignKey('safehouses.id'), index=True)
    packages = db.relationship('Package', back_populates='agent')
    x = db.Column(db.Integer,nullable=False, index=True)
    y = db.Column(db.Integer,nullable=False, index=True)
    alive = db.Column(db.Boolean, server_default='t', nullable=False)
    created_at =db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at =db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Agent %r>' % self.id

    def find(instance_id):
        # Find instance by id
        return Agent.query.filter(Agent.id == instance_id).first()

    def create(player,position):
        new_agent = Agent(player_id=player.id,x=position[0],y=position[1])
        db.session.add(new_agent)
        db.session.commit()
        return new_agent

    def has_packages(self):
        return len(self.packages) > 0

    def in_safehouse(self):
        return not self.safehouse_id == None

    def kill(self):
        self.alive = False
        [package.drop() for package in self.packages]
        db.session.commit()

    def legal_moves(self):
        moves = [(self.x+1,self.y),(self.x-1,self.y),(self.x, self.y+1),(self.x,self.y-1)]
        return [move for move in moves if move[0] > -1 and move[0] < 100 and move[1] > -1 and move[1] < 100]

    def serialize(self, requestor):
        if requestor == 'Alpha' and self.player.name == 'Alpha':
            return {'id': self.id, 'x': self.x, 'y': self.y, 'safehouse': self.in_safehouse(), 'packages': len(self.packages)}
        elif requestor == 'Charlie' and (self.player.name == 'Alpha' or self.player.name == 'Charlie'):
            return {'id': self.id, 'x': self.x, 'y': self.y}
        elif requestor == 'Bravo' and (self.player.name == 'Charlie'):
            return {'id': self.id, 'x': self.x, 'y': self.y}

    def leave_safehouse(self):
        self.safehouse_id = None
        db.session.commit()

    def enter_safehouse(self, safehouse):
        self.safehouse = safehouse
        db.session.commit()

    def move(self,x,y):
        if not self.alive:
            raise IsDead("Agent {agent_id} is dead".format(agent_id=self.id),404)
        if (x,y) not in self.legal_moves():
            raise IllegalMove(
                "Agent {agent_id} can't move to {x},{y}, only to [{legal_moves}]".format(
                    agent_id=self.id,
                    x=x,
                    y=y,
                    legal_moves=",".join([str(move) for move in self.legal_moves()])
                    ),
                404
                )
        self.x = x
        self.y = y
        db.session.commit()
        self.resolve_move()

    def resolve_move(self):

        if self.safehouse_id != None and self.player.name != "Charlie":
            self.leave_safehouse()

        # Quite a few things need to happen and we need to get the priority right
        #First is there any agents already here?
        other_agents = Agent.query.filter(Agent.x == self.x and Agent.y == self.y and Agent.id != self.id and Agent.alive == True).all()

        for agent in other_agents:
            if agent.player.name == "Charlie" and (self.player.name == "Bravo" or self.player.name == "Alpha"):
                self.kill()
                raise IsDead("Agent {agent_id} is dead".format(agent_id=self.id),404)
            elif self.player.name == "Charlie" and not agent.in_safehouse() and (agent.player.name == "Bravo" or agent.player.name == "Alpha"):
                agent.kill()

        if self.player.name == "Charlie":
            # Charlie does not care about packages or safehouses
            return True

        packages = Package.query.filter(Package.x == self.x and Package.y == self.y and Package.agent_id == None and Package.safehouse_id == None).all()
        [package.pickup(self) for package in packages]
        [package.move(self.x,self.y) for package in self.packages]

        safehouse = Safehouse.query.filter(Safehouse.x == self.x and Safehouse.y == self.y).first()

        if safehouse:
            self.enter_safehouse(safehouse)
            if safehouse.dropoff:
                [package.enter_safehouse(safehouse) for package in self.packages]

        return True
