from rvb import db
from rvb.models import *
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ResourceMissing, IsDead, IllegalMove

class Safehouse(db.Model):
    __tablename__ = 'safehouses'

    id = db.Column(db.Integer, primary_key=True)
    agents = db.relationship('Agent', back_populates='safehouse')
    packages = db.relationship('Package', back_populates='safehouse')
    x = db.Column(db.Integer,nullable=False, index=True)
    y = db.Column(db.Integer,nullable=False, index=True)
    dropoff = db.Column(db.Boolean, server_default='t', nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Safehouse %r>' % self.id

    def find(instance_id):
        # Find instance by id
        return Safehouse.query.filter(Safehouse.id == instance_id).first()

    def create(position, dropoff):
        new_safehouse = Safehouse(dropoff=dropoff,x=position[0],y=position[1])
        db.session.add(new_safehouse)
        db.session.commit()
        return new_safehouse

    def all():
        return Safehouse.query.all()

    def has_packages(self):
        return len(self.packages) > 0

    def serialize(self):
        return {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'dropoff': self.dropoff,
            'packages': len(self.packages)
            }
