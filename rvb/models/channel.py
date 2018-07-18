from rvb import db
from rvb.models import *
from rvb.db.base import Base
from datetime import datetime
from sqlalchemy import func

class Channel(db.Model, Base):
    __tablename__ = 'channels'

    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', back_populates='channel', lazy=True)
    listeners = db.relationship('Listener', back_populates='channel', lazy=True)
    created_at =db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at =db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Channel %r>' % self.name

    def create():
        new_channel = Channel()
        db.session.add(new_channel)
        db.session.commit()
        return True

    def has_listeners(self):
        return len(self.listeners) > 0
