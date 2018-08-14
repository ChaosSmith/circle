from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError

class UserGame(db.Model, Base):
    __tablename__ = 'users_games'

    id = db.Column(db.Integer, primary_key=True)
    # game = db.relationship("Game", back_populates="users")
    # user = db.relationship("User", back_populates="games")
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<RoleUser %r>' % self.id
