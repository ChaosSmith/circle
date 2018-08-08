from rvb import db
from rvb.models import *
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError

class RoleUser(db.Model, Base):
    __tablename__ = 'roles_users'

    id = db.Column(db.Integer, primary_key=True)
    role = db.relationship("Role", back_populates="users")
    user = db.relationship("User", back_populates="roles")
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<RoleUser %r>' % self.id
