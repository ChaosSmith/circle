from rvb import db
from rvb.models import *
from rvb.db import connect, drop, create, DATABASE

def recreate_db():
    engine = connect(None)
    drop(engine,DATABASE)
    create(engine,DATABASE)
    db.create_all()

def load_roles():
    Role.create(name="tester", description="Role For Debugging, Development, Testing, and QA")

def setup():
    load_roles()
