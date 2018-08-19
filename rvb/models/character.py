from rvb import db
from rvb.db.base import Base
from datetime import datetime
import random, math, json
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import text
from rvb.exceptions import ApiError
from rvb.models.encounter import Encounter

class Character(db.Model, Base):
    __tablename__ = 'characters'

    game = db.relationship('Game', back_populates='characters')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    user = db.relationship('User', back_populates='characters')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    encounters = db.relationship('Encounter', back_populates='character')
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
    skills = db.Column(JSONB, server_default='[]', nullable=False)

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
            if self.game.grid[y][x]["tile"] == "M" and self.game.grid[self.y][self.x]["tile"] != "M":
                return Encounter.build(self.game, self, x, y, "mountain", "Mountain Climbing")
            else:
                self.update(x=x,y=y)
                return None
        else:
            raise ApiError("Illegal Move", 400)

    def attribute_modifier(self, attribute):
        atr = getattr(self, attribute)
        if atr >= 10:
            return math.floor((atr - 10) / 2.0)
        else:
            return math.ceil((atr - 10) / 2.0)

    def lose_health(self, amount=0):
        # An effect
        self.update(health=self.health - amount)
        return "You lost {h} health!".format(h=amount)

    def move_to(self, x, y):
        self.update(x=x,y=y)
        return "You are now at {x}, {y}".format(x=x,y=y)

    def apply_effect(self, effect):
        func = getattr(self, effect["func"])
        return func(**effect["inputs"])

    def skill_check(self, skill_name):
        modifier = 0

        with open('./rvb/game_data/skills.json') as s:
            skill_list = json.load(s)

        skill = [skill for skill in skill_list if skill["name"] == skill_name][0]
        character_skill = [skill for skill in self.skills if skill["name"] == skill_name]

        if len(character_skill) > 0:
            character_skill = character_skill[0]
            modifier += Math.ceil(character_skill["level"] / 2.0)
        else:
            modifier -= 2 # Unskilled Penalty

        modifier += self.attribute_modifier(skill["attribute"])

        return random.randint(1,20) + modifier
