import pickle
import io

from debug import dbg
from player import Player
from console import Console

class Game():
    """The Game class contains a console and associated game state (e.g. player object for the console).
    
    Eventually this will grow to include a list of players, associated consoles, etc."""
    def __init__(self):
        self.cons = Console(game = self)
        self.user = Player("Joe Test", self.cons)
        self.user.set_description('Joe Test', 'Our test player named Joe')
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)
        self.cons.set_user(self.user)
        self.heartbeat_users = []

    def save_game(self, filename):
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try:
            f = open(filename, 'w+b')
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
            self.cons.write("Saved entire game to file %s" % filename)
            f.close()
        except:
            self.cons.write("Error writing to file %s" % filename)
            
    def load_game(self, filename):
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try: 
            f = open(filename, 'r+b')
        except FileNotFoundError:
            self.cons.write("Error, couldn't find file named %s" % filename)
        try:
            newgame = pickle.load(f)
            self.cons, self.user, self.heartbeat_users = newgame.cons, newgame.user, newgame.heartbeat_users
            self.cons.game = self
            self.cons.write("Restored game state from file %s" % filename)
        except PickleError:
            self.cons.write("Encountered error while pickling to file %s, game not saved." % filename)
        f.close()
        
        
    def register_heartbeat(self, obj):
        """Add the specified object (obj) to the heartbeat_users list"""
        self.heartbeat_users.append(obj)
    
    def beat(self):
        """call all of the registered heartbeat functions"""
        for h in self.heartbeat_users:
            h.heartbeat()

    def loop(self):
        while True:
            self.beat()
            cmd = self.cons.take_input('-> ')
            keep_going = self.cons.parser.parse(self.user, self.cons, cmd)
            if not keep_going:
                dbg.shut_down()
                break
