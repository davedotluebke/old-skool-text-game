import gametools

from debug import dbg
from thing import Thing
from container import Container
from action import Action

class Room(Container):
    """Create a room."""
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, pref_id, light=1, safe=False, indoor=False, mod=None):
        """Initialize the room. Set <light> level to 0 for a dark room."""
        Container.__init__(self, default_name, path=pref_id, pref_id=pref_id)
        self.exits = {}
        self.caution_taped_exits = {}
        self.set_max_weight_carried(4e9)
        self.set_max_volume_carried(3e9)
        self.fix_in_place("You can't move that!")
        self.closable = False
        self.default_light = light  # Can see and perceive emits when light level > 0
        self.monster_safe = safe
        self.indoor = indoor
        self.mod = mod
        self.versions[gametools.findGamePath(__file__)] = 1
    
    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def detach(self, room_path):
        '''Remove the room from Thing.ID_dict[] and moves all objects in the room 
        to nulspace (this removes references to the room instance, specifically 
        the location field of contained objects). This should be called preparatory
        to deleting or reloading the room.
        
        Returns True for success or False if the room is not in Thing.ID_dict[]'''
        try:
            room = Thing.ID_dict[room_path]
            for o in room.contents:
                o.move_to(Thing.ID_dict['nulspace'], force_move=True)
            del Thing.ID_dict[room_path]
            return True
        except KeyError:
            return False

    def add_exit(self, exit_name, exit_room, caution_tape_msg=False):
        self.exits[exit_name] = exit_room
        self.caution_taped_exits[exit_name] = caution_tape_msg
    
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

    def report_arrival(self, user, silent=False):
        if not user.cons:
            return
        loc = user.location
        cons = user.cons
        if not silent: 
            user.emit("&nI%s arrives." % user.id, [user])
        if loc.is_dark():
            cons.write("It's too dark to see anything here.")
            return True
        if user.terse:
            cons.write("You enter a %s." % loc._short_desc)
        else:
            cons.write(loc._long_desc)
        if (len(loc.exits) > 0):
            cons.write("Exits are:")
            for w in loc.exits:
                cons.write('\t' + w)
        else:
            cons.write("There are no obvious exits.")
        local_objects = ["&ni" + o.id for o in self.contents if o is not cons.user and not o.unlisted]
        if local_objects:
            cons.user.perceive("Here you see:\n\t" + '\n\t'.join(local_objects))         

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def move_to(self, p, cons, oDO, oIDO):
        return 'Rooms cannot be moved!'

    def look_at(self, p, cons, oDO, oIDO):
        """Print long description of room, list items (excluding this player) and exits"""
        # if verb is transitive, verify that the room is the direct object
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO and (oDO is None): 
            return "I'm not sure what you are trying to look at!"
        if self.is_dark():
            cons.user.perceive("It's too dark to see anything here.")
            return True
        cons.user.perceive(self._long_desc)
        if (len(self.exits) > 0):
            cons.user.perceive("Exits are:")
            for w in self.exits:
                cons.user.perceive('\t' + w)
        else:
            cons.user.perceive("There are no obvious exits.")            
        local_objects = ["&ni" + o.id for o in self.contents if o is not cons.user and not o.unlisted]
        if local_objects:
            cons.user.perceive("Here you see:\n\t" + '\n\t'.join(local_objects))
        
        return True

    def go_to(self, p, cons, oDO, oIDO):
        words = p.words
        user = cons.user
        sExit = words[1]  
        if sExit in list(self.exits):
            if self.caution_taped_exits[sExit]:
                cons.write(self.caution_taped_exits[sExit])
                return True
            try:
                destPath = self.exits[sExit]  # filename of the destination room module
                dest = gametools.load_room(destPath)
            except KeyError:
                dbg.debug("KeyError: exit '%s' maps to '%s' which is not an object in the game!" % (sExit, self.exits[sExit]), 0)
                cons.write("There was an internal error with the exit. ")
                return True
            if cons.user.move_to(dest):
                loc = user.location
                verb = words[0]
                conjugated = "goes" if verb == "go" else verb + 's'
                cons.write("You %s to the %s." % (verb, sExit))
                self.emit("&nD%s %s to the %s." % (user.id, conjugated, sExit))
                loc.report_arrival(user)
                return True
            else:
                return "For some reason you are unable to go to the %s." % sExit
        else: # user did not specify a valid exit
            return "I don't see how to go %s!" % sExit
    
    actions = dict(Container.actions)
    actions['look'] = Action(look_at, True, True)
    actions['examine'] = Action(look_at, True, True)
    actions['go'] = Action(go_to, True, False)
    actions['walk'] = Action(go_to, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def check_loaded(room_path):
    '''Check whether a room exists (i.e., has been created and inserted into Thing_ID.dict[]).
    Takes roomPath, the file of the room module as returned by gametools.findGamePath().
    Returns a reference to the room, or False if the room does not yet exist.'''
    if room_path in Thing.ID_dict:
        return Thing.ID_dict[room_path]
    else:
        return False