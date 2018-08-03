# import os
# import tempfile
#
# import pytest

from rvb.models import *

game = Game.find(1)
if game == None:
    game = Game.create(name="test", length=100, height=100)

village = Village.find(1)
if village == None:
    village = Village.create(x=10,y=10,population=100, food=100, game_id=1)

for _ in range(96*10):
    game.tick()
