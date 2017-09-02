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
nulspace = Room('nulspace', pref_id=None)         #"nulspace" is a room for objects that should be deleted. TODO: Automaticly delete items from nulspace every 10 heartbeats.
nulspace.game = game
nulspace.set_description('void', 'This is an empty void where dead and destroyed things go. Good luck getting out!')
nulspace.add_names('void')
nulspace.add_exit('north', 'nulspace')
nulspace.add_exit('south', 'nulspace')
nulspace.add_exit('east', 'nulspace')
nulspace.add_exit('west', 'nulspace')
game.events.schedule(game.time+5, game.clear_nulspace)
game.nulspace = nulspace

Thing.game = game

start_room_mod = importlib.import_module('domains.school.school.great_hall')
start_room = start_room_mod.load()
start_room.insert(game.user)

scroll = gametools.clone('domains.school.scroll')
scroll.move_to(game.user)
game.register_heartbeat(scroll)
game.user.set_start_loc = start_room
game.user.cons.write("\nWelcome to Firlefile Sorcery School!\n\n"
"Type 'look' to examine your surroundings or an object, "
"'inventory' to see what you are carrying, " 
"'quit' to end the game, and 'help' for more information.")
game.loop()

