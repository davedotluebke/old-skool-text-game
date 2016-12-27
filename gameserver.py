import pickle
import io

from debug import dbg
from thing import Thing
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
    '''
    def __getstate__(self):
        """Custom pickling code for Game. 
        
        First pickles Thing.ID_dict which references every object in the game.
        We only want to pickle this dictionary once, and we want to pickle it
        before pickling any of those objects.
        """
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        state['ID_dict'] = Thing.ID_dict.copy()
        # Remove the unpicklable entries.
        del state['cons']
        return state

    def __setstate__(self, state):
        """Custom unpickling code for Game.abs

        First unpickles and sets the new Thing.ID_dict, so unpickling later
        objects that refer to others by ID (such as Player.location) works.
        """
        # Restore instance attributes
        Thing.ID_dict = state['ID_dict']
        del state['ID_dict']
        # state.cons = self.cons
        self.__dict__.update(state)
    '''
    
    def save_game(self, filename):
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try:
            f = open(filename, 'w+b')
            pickle.dump(Thing.ID_dict, f, pickle.HIGHEST_PROTOCOL)
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
            return
        try:
            new_ID_dict = pickle.load(f)
            Thing.ID_dict = new_ID_dict
            newgame = pickle.load(f)
            self.user, self.heartbeat_users = newgame.user, newgame.heartbeat_users
            self.cons.game = self
            self.user.cons = self.cons  # custom pickling code for Player doesn't save console
            self.cons.user = self.user  # update backref from cons
            self.cons.write("Restored game state from file %s" % filename)
        except pickle.PickleError:
            self.cons.write("Encountered error while pickling to file %s, game not saved." % filename)
        f.close()
    
    def save_player(self, filename):
        pass

    def load_player(self, filename):
        
        room.report_arrival(self.cons, self, room)
        room.emit("%s suddenly appears, as if by sorcery!" % self)

        pass
        
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
