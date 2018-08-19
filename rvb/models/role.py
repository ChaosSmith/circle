from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random
from sqlalchemy import func
from rvb.exceptions import ApiError
from flask_security import RoleMixin

class Role(db.Model, Base, RoleMixin):
    __tablename__ = 'roles'

    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)
    users = db.relationship("RoleUser", back_populates="role")

    def __repr__(self):
        return '<Role %r>' % self.id
