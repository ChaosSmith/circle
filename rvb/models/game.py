from rvb import db
from rvb.models import *
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func

class Game(db.Model):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Game %r>' % self.id
