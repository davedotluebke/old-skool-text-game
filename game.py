from debug import dbg

from player import Player
from console import Console

class Game():
    """The Game class contains a console and associated game state (e.g. player object for the console).
    
    Eventually this will grow to include a list of players, associated consoles, etc."""
    def __init__(self):
        self.cons = Console()
        self.user = Player("testplayer", self.cons)
        self.user.set_description('joe test', 'our test player named joe')
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)
        self.cons.set_user(self.user)
        self.heartbeat_users = []

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
    
## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state and must be referenced by all the various objects. 
## 
game = Game()