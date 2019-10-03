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

argparser = argparse.ArgumentParser(description="Start the game server")
argparser.add_argument("-s", "--server", help="IP address at which the server will listen for clients")
argparser.add_argument("-m", "--mode", help="Whether or not to use https and ssl")
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

game = Game(ip, args.mode)

Thing.game = game

start_room_mod = importlib.import_module('domains.school.school.great_hall')
start_room = start_room_mod.load()
game.start_loop()

