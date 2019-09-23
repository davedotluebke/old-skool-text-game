import sys
import argparse
import ipaddress
import importlib
import traceback

from debug import dbg
import gametools

from gameserver import Game
from thing import Thing
from room import Room  
from console import Console

argparser = argparse.ArgumentParser(description="Start the game server for the Old Skool Text Adventure Game")
argparser.add_argument("-s", "--server", help="IP address at which the server should listen for clients")
args = argparser.parse_args()
if args.server:
    try:  # validate the ip address passed as an argument, if any
        ipaddress.ip_address(args.server)
        ip = args.server
    except ValueError:
        dbg.debug("Error: %s is not a valid IP address! Exiting..." % args.server)
        sys.exit("Invalid IP address specified on command line")
else:
    ip = None

## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state. 
## 
game = Game(ip)
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
game.start_loop()

