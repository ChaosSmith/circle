from rvb import db
from rvb.models import *
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError

class Package(db.Model):
    __tablename__ = 'packages'

    id = db.Column(db.Integer, primary_key=True)
    agent = db.relationship('Agent', back_populates='packages')
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), index=True)
    safehouse = db.relationship('Safehouse', back_populates='packages')
    safehouse_id = db.Column(db.Integer, db.ForeignKey('safehouses.id'), index=True)
    x = db.Column(db.Integer,nullable=False, index=True)
    y = db.Column(db.Integer,nullable=False, index=True)
    created_at =db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at =db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Package %r>' % self.id

    def find(instance_id):
        # Find instance by id
        return Package.query.filter(Package.id == instance_id).first()

    def all():
        return Package.query.all()

    def create(position):
        new_package = Package(x=position[0],y=position[1])
        db.session.add(new_package)
        db.session.commit()
        return new_package

    def in_safehouse(self):
        return not self.safehouse_id == None

    def pickup(self, agent):
        self.agent = agent
        db.session.commit()

    def drop(self):
        self.agent_id = None
        db.session.commit()

    def enter_safehouse(self, safehouse):
        self.safehouse = safehouse
        self.agent_id = None
        db.session.commit()

    def move(self,x,y):
        if x == self.x and y == self.y:
            # We are already here, don't waste db cycle
            return
        self.x = x
        self.y = y
        db.session.commit()

    def serialize(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'agent_id': self.agent_id,
            'in_safehouse': self.in_safehouse()
            }
