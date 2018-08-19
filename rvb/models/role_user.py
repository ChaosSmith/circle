from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError

class RoleUser(db.Model, Base):
    __tablename__ = 'roles_users'

    role = db.relationship("Role", back_populates="users")
    user = db.relationship("User", back_populates="roles")
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    def __repr__(self):
        return '<RoleUser %r>' % self.id
