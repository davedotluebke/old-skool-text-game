import importlib

from gameserver import Game
from thing import Thing
from room import Room 

def launch_default():
    """Launch the game with the default settings."""
    game = Game() # "game" is a special global variable, an object of class Game that holds the actual game state.
    nulspace = Room('nulspace', pref_id=None) #"nulspace" is a room for objects that should be deleted. 
    nulspace.game = game
    nulspace.set_description('void', 'This is an empty void where dead and destroyed things go. Good luck getting out!')
    nulspace.add_names('void')
    game.events.schedule(game.time+5, game.clear_nulspace)
    game.nulspace = nulspace

    Thing.game = game

    start_room_mod = importlib.import_module('domains.school.school.great_hall')
    start_room = start_room_mod.load()
    game.start_loop()

def launch_analysis():
    """Lauch in analysis mode. Results in higher debug frequency and additional speed timing."""
    game = Game() # "game" is a special global variable, an object of class Game that holds the actual game state.
    nulspace = Room('nulspace', pref_id=None) #"nulspace" is a room for objects that should be deleted. 
    nulspace.game = game
    nulspace.set_description('void', 'This is an empty void where dead and destroyed things go. Good luck getting out!')
    nulspace.add_names('void')
    game.events.schedule(game.time+5, game.clear_nulspace)
    game.nulspace = nulspace

    Thing.game = game

    start_room_mod = importlib.import_module('domains.school.school.great_hall')
    start_room = start_room_mod.load()
    game.begin_analysis_mode()


launch_cmds = {
    "default": {
        "type": "function",
        "function": launch_default,
        "complete": True
    },
    "help": {
        "type": "message",
        "message": "Please enter a startup command. 'Default' begins the game with the default settings.",
        "complete": False
    },
    "vscode": {
        "type": "function",
        "function": launch_default,
        "complete": True
    },
    "analysis": {
        "type": "function",
        "function": launch_analysis,
        "complete": True
    }
}
