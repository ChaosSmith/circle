from datetime import datetime

from rvb import db
from rvb.db.base import Base
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm.attributes import flag_modified
from rvb.lib.scenes import create_scenes
# from rvb.exceptions import ApiError

class Encounter(db.Model, Base):
    __tablename__ = 'encounters'

    game = db.relationship('Game', back_populates='encounters')
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False, index=True)
    character = db.relationship('Character', back_populates='encounters')
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False, index=True)
    title = db.Column(db.String, nullable=False)
    x = db.Column(db.Integer,nullable=False)
    y = db.Column(db.Integer,nullable=False)
    scenes = db.Column(JSONB, server_default='[]', nullable=False)
    current_scene = db.Column(db.Integer, server_default='0', nullable=False)
    completed_at = db.Column(db.TIMESTAMP)

    def build(game, character, x, y, source, title):
        scenes = create_scenes(game, character, x, y, source)
        encounter = Encounter.create(
            game_id = game.id,
            character_id = character.id,
            title = title,
            x = x,
            y = y,
            scenes = scenes
        )
        return encounter

    def __repr__(self):
        return '<Encounter %r>' % self.id

    def finished(self):
        return self.completed_at != None

    def send(self, option_id=None, resolve=False, roll=False, proceed=False ):
        if option_id:
            outcome = self.scenes[self.current_scene]["options"][int(option_id)]["outcome"]
            self.update(current_scene=outcome["go_to"])

        if resolve:
            self.update(completed_at=datetime.now())

        if roll:
            scene = self.scenes[self.current_scene]
            r = min(self.character.skill_check(scene["skill"]), 20)
            result = [result for result in scene["results"] if r in range(result["range"][0],result["range"][1]+1)][0]
            scene["rolled"] = True
            scene["roll"] = r
            scene["result"] = result
            messages = []
            for effect in result["effects"]:
                for key, val in effect["inputs"].items():
                    if val == "x":
                        effect["inputs"][key] = self.x
                    if val == "y":
                        effect["inputs"][key] = self.y
                messages.append(self.character.apply_effect(effect))
            scene["result"]["messages"] = messages
            self.scenes[self.current_scene] = scene
            flag_modified(self, "scenes")
            self.save()

        if proceed:
            scene = self.scenes[self.current_scene]
            result = [result for result in scene["results"] if scene["roll"] in range(result["range"][0],result["range"][1]+1)][0]
            self.update(current_scene=result["go_to"])
            scene = self.scenes[self.current_scene]
            for effect in scene["effects"]:
                for key, val in effect["inputs"].items():
                    if val == "x":
                        effect["inputs"][key] = self.x
                    if val == "y":
                        effect["inputs"][key] = self.y
                scene["messages"].append(self.character.apply_effect(effect))
