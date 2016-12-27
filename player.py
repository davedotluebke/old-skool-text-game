from thing import Thing
from room import Room
from creature import Creature
from action import Action

from debug import dbg

class Player(Creature):
    def __init__(self, ID, console):
        """Initialize the Player object and attach a console"""
        Creature.__init__(self, ID)
        self.cons = console
        self.set_weight(175/2.2)
        self.set_volume(66)
        inv = Action(self.inventory, "inventory", False, True)
        self.actions.append(inv)
    '''
    def __getstate__(self):
        """Custom pickling code for Player. 
        
        Avoids directly pickling the associated console (will eventually
        delete this for save-and-quit functionality in multiplayer; for 
        now just detach the console to support save-and-keep-playing). 

        Avoids directly pickling the player's location, instead returning 
        the location's (presumed unique) ID for lookup in Thing.ID_dict."""
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        if self.id == "Joe Test": # XXX temp for debugging purposes
            dbg.debug("Pickling Joe Test!")
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['cons']
        del state['location']
        state['locationID'] = self.location.id
        return state

    def __setstate__(self, state):
        """Custom unpickling code for Player

        Set the location to the (Room) object indicated by the stored ID.
        Eventually, when multiplayer works, the function unpickling the 
        Player will then attach it to a new console."""
        if (state['id'] == "Joe Test"):
            dbg.debug("Unpickling Joe Test!")
        # Restore instance attributes
        room_id = state['locationID']
        room = Thing.ID_dict[room_id]
        del state['locationID']
        self.__dict__.update(state)
        self.location = None  # use move_to so room is updated correctly
        self.move_to(room)
'''

    def perceive(self, message):
        if not self.location.is_dark():
            Creature.perceive(self, message)
            self.cons.write(message)        

    def inventory(self, p, cons, oDO, oIDO):
        cons.write("You are carrying:")
        if not self.contents:
            cons.write('nothing')
        for i in self.contents:
            cons.write("a " + i.short_desc)
        return True

