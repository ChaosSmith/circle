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
        return cls.query.filter(csl.id == instance_id).first()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.query.filter(kwargs).first()

    def update(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        try:
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False
