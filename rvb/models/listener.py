from rvb import db
from rvb.models import *
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError

class Listener(db.Model):
    __tablename__ = 'listeners'

    id = db.Column(db.Integer, primary_key=True)
    channel = db.relationship('Channel', back_populates='listeners')
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    messages = db.relationship('Message', back_populates='listener', lazy=True)
    created_at =db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at =db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Listener %r>' % self.id

    def find(instance_id):
        # Find instance by id
        return Listener.query.filter(Listener.id == instance_id).first()

    def create():
        new_listener = Listener()
        db.session.add(new_listener)
        db.session.commit()
        return True

    def listen_to(self, channel_id):
        channel = Channel.query.filter(Channel.id == channel_id).first()

        if channel:
            self.channel = channel
            db.session.commit()
            return True
        else:
            raise ApiError("No channel found with id %r" % channel_id,404)

    def serialize_messages(self):
        return [message.serialize() for message in self.messages]

    def decrypt_level(self):
        intercepts = len(self.messages)
        if intercepts >= 10:
            return 1
        elif intercepts == 0:
            return 0
        else:
            return intercepts / 10.0
