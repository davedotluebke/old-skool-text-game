import importlib
import traceback
from debug import dbg
import gametools

from gameserver import Game
from thing import Thing
from room import Room  
from console import Console

## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state. 
## 
game = Game()

Thing.game = game

start_room_mod = importlib.import_module('domains.school.school.great_hall')
start_room = start_room_mod.load()
game.start_loop()

