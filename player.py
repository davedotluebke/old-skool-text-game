import pickle
import sys

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
        self.start_loc_id = None
        self.set_weight(175/2.2)
        self.set_volume(66)
        self.actions.append(Action(self.inventory, "inventory", False, True))
        self.actions.append(Action(self.execute, "execute", True, True))
        
    def __getstate__(self):
        """Custom pickling code for Player. 
        
        Avoids directly pickling the associated console (will eventually
        delete this for save-and-quit functionality in multiplayer; for 
        now just detach the console to support save-and-keep-playing). 
        """
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        if self.id == "Joe Test": # XXX temp for debugging purposes
            dbg.debug("Pickling Joe Test!")
        clone_contents = []
        r_contents = self.contents
        for i in self.contents:
            clone_contents.append(i.clone_code('cloned'))
        self.contents = clone_contents
        state = super().__getstate__()
        # Remove the unpicklable entries.
        del state['cons']
        self.contents = r_contents
        return state

    def __setstate__(self, state):
        """Custom unpickling code for Player

        Note 1: The function unpickling the Player must then attach it to
        a new console.
        
        Note 2: If the player is joining an ongoing game (as opposed to the
        entire game including players getting saved/restored) then the 
        function unpickling the player should restore the location field from
        an ID string to a direct reference, do the same for the objects in the
        contents field, and call move_to() to update the room."""
        super(Player, self).__setstate__(state) # updates Thing.ID_dict
        if (state['id'] == "Joe Test"):
            dbg.debug("Unpickling Joe Test!")
        # Restore instance attributes
        self.short_desc = "Clone of " + self.short_desc # XXX temp for debugging

    def set_start_loc(self, startroom):
        self.start_loc_id = startroom.id

    def die(self, message):
        Creature.die(self, message)
        self.cons.write("You have died!\n\nFortunately you are reincarnated immediately...")
        self.health = self.hitpoints
        if (self.start_loc_id):
            room = Thing.ID_dict[self.start_loc_id]
            self.move_to(room)
            room.report_arrival(self)
        else:
            self.cons.write("Uh-oh! You don't have a starting location. You are in a great void...")

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
    
    def execute(self, p, cons, oDO, oIDO):
        cmd = ' '.join(p.words[1:])
        cons.write("Executing command: '%s'" % cmd)
        try: 
            exec(cmd)
        except Exception as inst:
            cons.write("Unexpected error: " + str(sys.exc_info()[0]) + "\n\t" + str(sys.exc_info()[1]))
            # cons.write(type(inst)+"\n"+inst)    # the exception instance
        return True

    def hold_object(self, obj):
        self.visible_inventory.append(obj)
