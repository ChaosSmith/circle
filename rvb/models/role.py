from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError
from flask_security import RoleMixin

class Role(db.Model, Base, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)
    users = db.relationship("RoleUser", back_populates="role")

    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Role %r>' % self.id
