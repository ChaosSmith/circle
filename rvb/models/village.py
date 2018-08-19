import math
import random

from rvb import db
from rvb.db.base import Base
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError
from rvb.utils import season_food, season_map

class Village(db.Model, Base):
    __tablename__ = 'villages'

    game = db.relationship('Game', back_populates='villages')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    x = db.Column(db.Integer,nullable=False)
    y = db.Column(db.Integer,nullable=False)
    food = db.Column(db.Integer, server_default="0", nullable=False)
    population = db.Column(db.Integer, server_default="0", nullable=False)

    def __repr__(self):
        return '<Village %r>' % self.id

    def tick(self):
        pass

    def new_day(self, season):
        consumption = self.compute_food_consumption()
        production = self.compute_food_production(season)
        self.update(
            food=(self.food-consumption+production),
            )
        print(season_map[season])
        print("Village produced {p}, ate {c}, now has {t} food".format(c=consumption, p=production, t=self.food))

    def new_season(self):
        growth = self.compute_growth()
        self.update(
            population=(self.population+growth),
            )
        print("Village population changed by {g} people".format(g=growth))

    def compute_growth(self):
        return math.floor(self.population * random.gauss(0.01, 0.01))

    def compute_food_production(self, season):
        return max([0,math.floor(self.population * random.gauss(season_food[season], 1))])

    def compute_food_consumption(self):
        return self.population
