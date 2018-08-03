import math

from rvb import db
from rvb.db.base import Base
from datetime import datetime
from sqlalchemy import func
from flask import json
from rvb.exceptions import ApiError
from rvb.utils import season_map

class Game(db.Model, Base):
    __tablename__ = 'games'

    id = db.Column(db.Integer, primary_key=True)
    charcters = db.relationship('Character', back_populates='game')
    villages = db.relationship('Village', back_populates='game')
    name = db.Column(db.String, nullable=False)
    length = db.Column(db.Integer,nullable=False)
    height = db.Column(db.Integer,nullable=False)
    ticks = db.Column(db.Integer, server_default="0")
    last_tick_at = db.Column(db.TIMESTAMP)
    created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    updated_at = db.Column(db.TIMESTAMP, server_default=func.now(),onupdate=func.current_timestamp())

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
