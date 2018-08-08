import math
import random

from rvb import db
from rvb.db.base import Base
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError
from rvb.utils import season_map
from rvb.models.village import Village

class Game(db.Model, Base):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    users = db.relationship("User", secondary="users_games", back_populates="games")
    characters = db.relationship('Character', back_populates='game')
    villages = db.relationship('Village', back_populates='game')
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    length = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Integer,nullable=False)
    ticks = db.Column(db.Integer, server_default="0")
    last_tick_at = db.Column(db.TIMESTAMP)
    active = db.Column(db.Boolean, server_default='f')
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

    def new_game(creator, villages, length, height, name, password):
        new_game = Game.create(name=name,height=height,length=length, password=password)
        new_game.spawn_villages(villages)
        creator.join_game(new_game.id)

    def __repr__(self):
        return '<Game %r>' % self.id

    def spawn_villages(self, number):
        for _ in range(number):
            x = random.randint(0,self.length)
            y = random.randint(0,self.height)
            Village.create(x=x, y=y, population=100, food=100, game_id=self.id)

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

    def display(self):
        villages = self.villages
        grid = []
        for x in range(self.length):
            grid.append([])
            for y in range(self.height):
                for village in villages:
                    if village.x == x and village.y == y:
                        grid[x].append("V")
                        break
                if len(grid[x]) == y+1:
                    continue
                else:
                    grid[x].append(" ")
        return grid
