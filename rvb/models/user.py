from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError
from flask_security import UserMixin

class User(db.Model, Base, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean)
    confirmed_at = db.Column(db.TIMESTAMP)
    roles = db.relationship("RoleUser", back_populates="user")
    games = db.relationship("Game", secondary="users_games", back_populates="users")
    characters = db.relationship('Character', back_populates='user')
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<User %r>' % self.id

    def add_role(self, role):
        RoleUser.create(user_id=self.id, role_id=self.id)

    def join_game(self, game_id):
        from rvb.models.user_game import UserGame
        UserGame.create(user_id=self.id, game_id=game_id)
