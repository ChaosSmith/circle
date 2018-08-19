import math
import random

from rvb import db
from rvb.db.base import Base
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError
from rvb.utils import season_map
from rvb.lib.grid import build_grid

class Game(db.Model, Base):
    __tablename__ = 'games'

    users = db.relationship("User", secondary="users_games", back_populates="games")
    characters = db.relationship('Character', back_populates='game')
    villages = db.relationship('Village', back_populates='game')
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    width = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Integer,nullable=False)
    ticks = db.Column(db.Integer, server_default="0")
    last_tick_at = db.Column(db.TIMESTAMP)
    grid = db.Column(db.JSON, nullable=False, server_default='[]')
    active = db.Column(db.Boolean, server_default='f')

    def new_game(creator, villages, width, height, name, password):
        game = Game.create(name=name,height=height,width=width, password=password)
        grid = build_grid(width, height, game.id, 4, 80, villages)
        game.update(grid=grid)
        creator.join_game(game.id)
        return game

    def __repr__(self):
        return '<Game %r>' % self.id

    def tick(self):

        self.update(
            ticks=(self.ticks + 1),
            last_tick_at=datetime.now()
            )

        if self.is_new_season():
            # All hooks for new season originate here
            for village in self.villages:
                village.new_season()

        if self.is_new_day():
            # All hooks for new days originate here
            for village in self.villages:
                village.new_day(self.date()['season'])

        # Tick hooks originate here
        for village in self.villages:
            village.tick()
        for character in self.characters:
            character.tick()

    def is_new_season(self):
        return (self.ticks) % 96 == 0

    def is_new_day(self):
        return (self.ticks) % 8 == 0

    def date(self):
        year = math.floor(self.ticks / (96*4)) + 1
        season = math.floor((self.ticks % (96*4)) / 96)
        day = math.floor((self.ticks % 96) / 8) + 1
        hour = (self.ticks % 8) * 3
        return {"year": year, "season": season, "day": day, "hour": hour}

    def print_date(self):
        date = self.date()
        print("The date is now year: {y}, season: {s}, day: {d}, hour: {h}".format(
                y=date['year'],
                s=season_map[date['season']],
                d=date['day'],
                h=date['hour']
                )
            )

    def display(self, viewer=None):
        villages = self.villages
        characters = self.characters
        if viewer:
            legal_moves = viewer.legal_moves()
        grid = self.grid
        for row in grid:
            for tile in row:
                for character in characters:
                    if character.x == tile["x"] and character.y == tile["y"]:
                        tile["tile"] = "P"
                        break
                if viewer:
                    for move in legal_moves:
                        if move[0] == tile["x"] and move[1] == tile["y"]:
                            tile["move"] = True

        return grid
