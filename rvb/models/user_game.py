from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError

class UserGame(db.Model, Base):
    __tablename__ = 'users_games'

    # game = db.relationship("Game", back_populates="users")
    # user = db.relationship("User", back_populates="games")
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    def __repr__(self):
        return '<RoleUser %r>' % self.id
