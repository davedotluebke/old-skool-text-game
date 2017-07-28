import importlib

from debug import dbg
from thing import Thing
from container import Container
from action import Action

def check_loaded(roomPath):
        '''Check whether a room exists (i.e., has been created and inserted into Thing_ID.dict[]).
        Takes roomPath, the file of the room module as returned by gametools.findGamePath().
        Returns a reference to the room, or False if the room does not yet exist.'''
        if roomPath in Thing.ID_dict:
            return Thing.ID_dict[roomPath]
        else:
            return False

class Room(Container):
    def __init__(self, default_name, light=1, safe=False, pref_id=None):
        """Initialize the room. Set <light> level to 0 for a dark room."""
        Container.__init__(self, default_name, path=pref_id, pref_id=pref_id)
        self.exits = {}
        self.enters = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.actions.append(Action(self.go_to, ["go", "walk"], True, False))
        self.actions.append(Action(self.look_at, ["look", "examine"], True, True))
        self.actions.append(Action(self.enter, ["enter"], True, False))
        self.fix_in_place("You can't move that!")
        self.closable = False
        self.default_light = light  # Can see and perceive emits when light level > 0
        self.monster_safe = safe

    def add_exit(self, exit_name, exit_room):
        self.exits[exit_name] = exit_room
    
    def add_enter(self, enter_name, enter_room):
        self.enters[enter_name] = enter_room

    def is_dark(self):
        total_light = self.default_light
        obj_list = self.contents[:]
        for obj in obj_list:
            if hasattr(obj, 'light'):
                total_light += obj.light
            # recursively check for lights inside containers or players
            if isinstance(obj, Container) and (obj.see_inside or hasattr(obj, 'cons')):
                if obj.contents: 
                    obj_list += obj.contents 
            dbg.debug('Room %s: light level is %s' % (self.id, total_light), 3)
        return (total_light <= 0)
        
    def look_at(self, p, cons, oDO, oIDO):
        """Print long description of room, list items (excluding this player) and exits"""
        # if verb is transitive, verify that the room is the direct object
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO and (oDO is None): 
            return "I'm not sure what you are trying to look at!"
        if self.is_dark():
            cons.write("It's too dark to see anything here.")
            return True
        cons.write(self.long_desc)
        assert(cons.user in self.contents)  # current player should always be in the room 
        if (len(self.exits) > 0):
            cons.write("Exits are:")
            for w in self.exits:
                cons.write('\t' + w)
            local_objects = ["a " + str(o) for o in self.contents if o is not cons.user]
            if local_objects:
                cons.write("Here you see:\n\t" + '\n\t'.join(local_objects))
        else:
            cons.write("There are no obvious exits.")
        return True

    def move_to(self, p, cons, oDO, oIDO):
        cons.write('rooms cannot be moved!')
    
    def report_arrival(self, user):
        loc = user.location
        cons = user.cons
        if loc.is_dark():
            cons.write("It's too dark to see anything here.")
            return True
        cons.write("You enter a %s." % loc.short_desc)
        if (len(loc.exits) > 0):
            cons.write("Exits are:")
            for w in loc.exits:
                cons.write('\t' + w)
            local_objects = ["a " + str(o) for o in loc.contents if o is not user]
            if local_objects:
                cons.write("Here you see:\n\t" + '\n\t'.join(local_objects))
        else:
            cons.write("There are no obvious exits.")

    def enter(self, p, cons, oDO, oIDO):
        words = p.words
        del words[0]
        words = words
        sEnter = ''
        b = False
        for i in words:
            if b:
                sEnter += ' '
            sEnter += i.lower()
            b = True
        if sEnter in list(self.enters):
            dest = Thing.ID_dict[self.enters[sEnter]]
            if cons.user.move_to(dest):
                loc = cons.user.location
                cons.write("You enter %s" % sEnter.capitalize())
                self.emit("%s enters %s" % (str(cons.user), sEnter.capitalize()))
                loc.report_arrival(cons.user)
                return True
            else:
                return "For some reason you are unable to enter %s." % sEnter.capitalize()
        else:
            return "I don't see anywhere named %s you can enter!" % sEnter.capitalize()

    def go_to(self, p, cons, oDO, oIDO):
        words = p.words
        user = cons.user
        sExit = words[1]  
        if sExit in list(self.exits):
            try:
                destFile = self.exits[sExit]  # filename of the destination room module
                destMod = importlib.import_module(destFile)  # python module of the destination room
                dest = destMod.load()
            except KeyError:
                dbg.debug("KeyError: exit '%s' maps to '%s' which is not an object in the game!" % (sExit, self.exits[sExit]), 0)
                cons.write("There was an internal error with the exit. ")
                return True
            if cons.user.move_to(dest):
                loc = user.location
                verb = words[0]
                conjugated = "goes" if verb == "go" else verb + 's'
                cons.write("You %s to the %s." % (verb, sExit))
                self.emit("%s %s to the %s." % (str(user), conjugated, sExit))
                loc.report_arrival(user)
                return True
            else:
                return "For some reason you are unable to go to the %s." % sExit
        else: # user did not specify a valid exit
            return "I don't see how to go %s!" % sExit
