from debug import dbg

from gameserver import Game
from action import Action
from thing import Thing
from container import Container
from room import Room  
from creature import Creature 
from creature import NPC
from player import Player
from console import Console
from scenery import Scenery
from liquid import Liquid
from weapon import Weapon
from armor import Armor
from book import Book

## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state. 
## 
game = Game()
nulspace = Room('nulspace')         #"nulspace" is a room for objects that should be deleted. TODO: Automaticly delete items from nulspace every 10 heartbeats.
nulspace.game = game
nulspace.set_description('void', 'This is an empty void where dead and destroyd things go. Good luck getting out!')
nulspace.add_names('void')
nulspace.add_exit('north', nulspace)
nulspace.add_exit('south', nulspace)
nulspace.add_exit('east', nulspace)
nulspace.add_exit('west', nulspace)

import domains.wizardry.galsbilly

import domains.school.forest as forest
import domains.school.school as school
import domains.school.dungeon as dungeon
import domains.school.cave as cave
import domains.school.waterfall as waterfall

import home.owen.house

cave.cave_entrance.add_aditional_vars(forest.forest_three, game)
cave.cave.add_exit('east', forest.forest_three)
cave.cave_entrance.add_exit('east', forest.forest_three)
game.register_heartbeat(cave.cave)
dungeon.crawlway.add_exit('southeast', cave.lair)
forest.forest_three.add_exit('west', cave.cave_entrance)

Thing.ID_dict['great hall'].insert(game.user)
Thing.ID_dict['scroll'].move_to(game.user)
game.register_heartbeat(Thing.ID_dict['scroll'])
game.user.set_start_loc = Thing.ID_dict['great hall']
game.user.cons.write("\nWelcome to Firlefile Sorcery School!\n\n"
"Type 'look' to examine your surroundings or an object, "
"'inventory' to see what you are carrying, " 
"'quit' to end the game, and 'help' for more information.")
game.loop()

