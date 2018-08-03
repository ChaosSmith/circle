from rvb import db

class Base:

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

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
