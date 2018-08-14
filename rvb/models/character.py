from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random, math
from sqlalchemy import func, text
from rvb.exceptions import ApiError

class Character(db.Model, Base):
    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    game = db.relationship('Game', back_populates='characters')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    user = db.relationship('User', back_populates='characters')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    actions = db.Column(db.Integer)
    x = db.Column(db.Integer,nullable=False)
    y = db.Column(db.Integer,nullable=False)
    strength = db.Column(db.Integer)
    constitution = db.Column(db.Integer)
    dexterity = db.Column(db.Integer)
    charisma = db.Column(db.Integer)
    wisdom = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    experience = db.Column(db.Integer, server_default=text("0"))
    max_health = db.Column(db.Integer)
    health = db.Column(db.Integer)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def __repr__(self):
        return '<Character %r>' % self.id

    def build(user, game, form):
        con = form.constitution.data
        if con >= 10:
            max_health = 10 + math.floor((form.constitution.data - 10) / 2.0)
        else:
            max_health = 10 + math.ceil((form.constitution.data - 10) / 2.0)

        character = Character.create(
            game_id=game.id,
            user_id=user.id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            max_health=max_health,
            health=max_health,
            strength=form.strength.data,
            dexterity=form.dexterity.data,
            constitution=form.constitution.data,
            charisma=form.charisma.data,
            wisdom=form.wisdom.data,
            intelligence=form.intelligence.data,
            x=0,
            y=0,
            actions=45
            )

        return character

    def tick(self):
        self.update(actions=self.actions+1)

    def legal_moves(self):
        moves = [(self.x+1,self.y),(self.x-1,self.y),(self.x, self.y+1),(self.x,self.y-1)]
        return [move for move in moves if move[0] > -1 and move[0] <= self.game.width and move[1] > -1 and move[1] <= self.game.height]

    def move(self,x,y):
        if (x,y) in self.legal_moves():
            self.update(x=x,y=y)
        else:
            raise ApiError("Illegal Move", 400)
