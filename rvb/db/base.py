from rvb import db
from sqlalchemy import func, text

class Base:

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        try:
            db.session.commit()
            print("It Did Commit")
        except e:
            print("Its going to rollback")
            print(e)
            db.session.rollback()
        finally:
            return instance

    @classmethod
    def find(cls, instance_id):
        return cls.query.filter(cls.id == instance_id).first()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def where(cls, **kwargs):
        return cls.query.filter_by(**kwargs).all()

    @classmethod
    def size(cls):
        return cls.query.count()

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def first(cls):
        return cls.query.first()

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
