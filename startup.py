
import sys
import argparse
import ipaddress
import importlib

import gametools

from gameserver import Game
from thing import Thing
from room import Room  

argparser = argparse.ArgumentParser(description="Start the game server")
argparser.add_argument("-s", "--server", help="IP address at which the server will listen for clients")
argparser.add_argument("-d", "--duration", help="How long to run before shutting down")
argparser.add_argument("-p", "--port", help="The port which to serve the game on; defaults to 9123")
argparser.add_argument("-r", "--retry", help="The number of times to retry (waiting 30s first) if the port is busy; defaults to 5")
args = argparser.parse_args()
if args.server:
    try:  # validate the ip address passed as an argument, if any
        ipaddress.ip_address(args.server)
        ip = args.server
    except ValueError:
        gametools.get_game_logger("_startup").critical("Error: %s is not a valid IP address! Exiting..." % args.server)
        sys.exit("Invalid IP address specified on command line")
else:
    ip = None

duration = args.duration if args.duration else 24*60*60 - 1  # One minute less than a single day
port = args.port if args.port else 9123
retry = args.retry if args.retry else 5

## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state. 
## 

game = Game(ip, duration, port, retry)

Thing.game = game

start_room_mod = importlib.import_module('domains.school.school.great_hall')
start_room = start_room_mod.load()
game.start_loop()

