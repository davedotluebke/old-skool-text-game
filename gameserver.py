import pickle
import io
import traceback

import gametools

from debug import dbg
from thing import Thing
from player import Player
from console import Console
from event_nsl import EventQueue

class Game():
    """The Game class contains a console and associated game state (e.g. player object for the console).
    
    Eventually this will grow to include a list of players, associated consoles, etc."""
    def __init__(self):
        self.heartbeat_users = []
        self.cons = Console(game = self)
        self.user = Player("Joe Test", None, self.cons)
        self.user.set_description('Joe Test', 'Our test player named Joe')
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)
        self.cons.set_user(self.user)
        self.events = EventQueue()
        self.time = 0

    def save_game(self, filename):
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try:
            f = open(filename, 'w+b')
            # explicitly dump ID_dict to guarantee we dump all objects
            save = Thing.ID_dict, self
            pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
            self.cons.write("Saved entire game to file %s" % filename)
            f.close()
        except IOError:
            self.cons.write("Error writing to file %s" % filename)
        except pickle.PickleError:
            self.cons.write("Error pickling when saving to file %s" % filename)
            
    def load_game(self, filename):
        if not filename.endswith('.OAD'): 
            filename += '.OAD'
        try:
            f = open(filename, 'r+b')
        except FileNotFoundError:
            self.cons.write("Error, couldn't find file named %s" % filename)
            return
        try:
            backup_ID_dict = Thing.ID_dict.copy()
            Thing.ID_dict.clear()  # unpickling will re-create Thing.ID_dict
            saved = pickle.load(f)
            new_ID_dict, newgame = saved
        except pickle.PickleError:
            self.cons.write("Encountered error while loading from file %s, game not loaded." % filename)
            Thing.ID_dict = backup_ID_dict
            f.close()
            return
        del backup_ID_dict
        
        # TODO: move below code for deleting player to Player.__del__()
        # Unlink player object from room, contents:
        if self.user.location.extract(self.user):
            dbg.debug("Error deleting player from room during load_game()")
        for o in self.user.contents: 
            if self.user.extract(o):
                dbg.debug("Error deleting contents of player (%s) during load_game()" % o)
        self.cons.user = None
        
        self.user, self.heartbeat_users = newgame.user, newgame.heartbeat_users
        self.user.cons = self.cons  # custom pickling code for Player doesn't save console
        self.cons.user = self.user  # update backref from cons

        for o in Thing.ID_dict: 
            Thing.ID_dict[o]._restore_objs_from_IDs()
            
        self.cons.write("Restored game state from file %s" % filename)
    
        f.close()
    
    def save_player(self, filename):
        # Uniquify the ID string of every object carried by the player
        tag = 'saveplayer'+str(random.randint(100000,999999))
        l = [self.user] 
        for obj in l:
            obj.id = obj.id + tag
            if obj.contents != None:
                l += obj.contents

        if not filename.endswith('.OADplayer'): 
            filename += '.OADplayer'
        try:
            f = open(filename, 'w+b')
            pickle.dump(l, f, pickle.HIGHEST_PROTOCOL)
            self.cons.write("Saved player data to file %s" % filename)
            f.close()
        except IOError:
            self.cons.write("Error writing to file %s" % filename)
        except pickle.PickleError:
            self.cons.write("Error pickling when saving to file %s" % filename)
        

    def load_player(self, filename):
        """Unpickle a single player and his/her inventory from a saved file.

        Objects in the player's inventory (and their contents, recursively) 
        are treated as new objects, and will often be duplicates of
        existing objects already in the game. Thus after unpickling each 
        object we need to add it to Thing.ID_dict with a new and unique ID.""" 

        if not filename.endswith('.OADplayer'): 
            filename += '.OADplayer'
        try:
            f = open(filename, 'r+b')
        except FileNotFoundError:
            self.cons.write("Error, couldn't find file named %s" % filename)
            return
        try:
            del Thing.ID_dict[self.user.id]  # unpickling will re-create Thing.ID_dict entry for new Player object
            l = pickle.load(f)
            f.close()
        except pickle.PickleError:
            self.cons.write("Encountered error while pickling to file %s, player not saved." % filename)
            Thing.ID_dict[self.user.id] = self.user
            f.close()
            return
        newplayer = l[0]
        # TODO: move below code for deleting player to Player.__del__()
        # Unlink player object from room, contents:
        if self.user.location.extract(self.user):
            dbg.debug("Error deleting player from room during load_game()")
        for o in self.user.contents: 
            if self.user.extract(o):
                dbg.debug("Error deleting contents of player (%s) during load_game()" % o)
        self.cons.user = None
        
        self.user = newplayer
        self.user.cons = self.cons  # custom pickling code for Player doesn't save console
        self.cons.user = self.user  # update backref from cons

        self.user.location = gametools.load(self.user.location) # XXX protect for case where saved room no longer exists

        # Create new entries in ID_dict for objects player is holding, 
        # and make sure that those objects refer to each other by the new IDs
        newIDs = {}  # mapping from ID strings stored with objs to new ID strings
        objs = self.user.contents
        for o in objs: 
            o._add_ID(preferred_id = o.id)  # XXX this won't work, contents were pickled as strings not original objects. 
            raise
            if o.contents != None:
                objs += o.contents
            
        room = self.user.location
        room.insert(self.user)  # insert() does some necessary bookkeeping
        self.cons.write("Restored game state from file %s" % filename)
        room.report_arrival(self.user)
        room.emit("%s suddenly appears, as if by sorcery!" % self.user, [self.user])

    def reload(self, filename):
        pass
        #filename

    def register_heartbeat(self, obj):
        """Add the specified object (obj) to the heartbeat_users list"""
        self.heartbeat_users.append(obj)
    
    def beat(self):
        """Advance time, run scheduled events, and call registered heartbeat functions"""
        self.time += 1

        current_events = self.events.check_for_event(self.time)
        for event in current_events:
            try:
                event.callback(event.payload)
            except Exception as inst:
                dbg.debug("An error occured while attepting to complete event (timestamp %s, callback %s, payload %s)! Printing below:" % (event.timestamp, event.callback, event.payload), 0)
                dbg.debug(traceback.format_exc(), 0)
                dbg.debug('Error caught!', 0)

        for h in self.heartbeat_users:
            try:
                h.heartbeat()
            except Exception as inst:
                dbg.debug("An error occured inside code for %s! Printing below:" % h, 0)
                dbg.debug(traceback.format_exc(), 0)
                dbg.debug('Error caught!', 0)

    def loop(self):
        while True:
            self.beat()
            cmd = self.cons.take_input('-> ')
            keep_going = self.cons.parser.parse(self.user, self.cons, cmd)
            if not keep_going:
                dbg.shut_down()
                break

    def clear_nulspace(self, x): #XXX temp problem events always returns a payload, often None.
        for i in self.nulspace.contents:
            if not hasattr(i, 'cons'): #if it is not player
                i.delete()
        self.events.schedule(self.time+5, self.clear_nulspace)
