import pickle
import sys

import gametools
from debug import dbg

from thing import Thing
from room import Room
from creature import Creature
from action import Action


class Player(Creature):
    def __init__(self, ID, path, console):
        """Initialize the Player object and attach a console"""
        Creature.__init__(self, ID, path)
        self.cons = console
        self.start_loc_id = None
        self.set_weight(175/2.2)
        self.set_volume(66)
        self.actions.append(Action(self.inventory, "inventory", False, True))
        self.actions.append(Action(self.toggle_terse, "terse", False, True))
        self.actions.append(Action(self.execute, "execute", True, True))
        self.actions.append(Action(self.fetch, "fetch", True, True))
        self.actions.append(Action(self.clone, "clone", True, True))
        self.actions.append(Action(self.apparate, "apparate", True, True))
        self.actions.append(Action(self.engage, "engage", True, False))
        self.actions.append(Action(self.disengage, "disengage", False, True))
        self.aggressive = 1         #TODO: Specilized individual stats
        self.armor_class = 10
        self.combat_skill = 40
        self.strength = 20
        self.dexterity = 60
        self.attack_now = 0
        self.wizardry_skill = 0
        self.wizardry_element = 'fire' #XXX: Temp until player setup finished
        self.attacking = False
        self.reading = False
        self.hitpoints = 20
        self.health = 20
        self.terse = False  # True -> show short description when entering room
        self.cons.game.register_heartbeat(self)

    def __getstate__(self):
        """Custom pickling code for Player. 
        
        Avoids directly pickling the associated console (will eventually
        delete this for save-and-quit functionality in multiplayer; for 
        now just detach the console to support save-and-keep-playing). 
        """
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = super().__getstate__()
        # Remove the unpicklable entries.
        del state['cons']
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
        # Restore instance attributes
        self.short_desc = "Clone of " + self.short_desc # XXX temp for debugging

    def set_start_loc(self, startroom):
        self.start_loc_id = startroom.id

    def heartbeat(self):
        if True:            # TODO: Player Prefrences
            if self.attacking:
                if self.attacking == 'quit':
                    return
                else:
                    self.attack_enemy(self.attacking)
            for i in self.location.contents:
                if i in self.enemies:
                    self.cons.write('You attack your enemy %s' % i.short_desc)
                    self.attacking = i
                    self.attack_enemy(i)

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
                   
    def hold_object(self, obj):
        self.visible_inventory.append(obj)

    #
    # ACTION FUNCTIONS (verbs):
    # 
    def inventory(self, p, cons, oDO, oIDO):
        cons.write("You are carrying:")
        if not self.contents:
            cons.write('\tnothing')
        for i in self.contents:
            if i == self.weapon_wielding or i == self.armor_worn: 
                continue
            cons.write("\ta " + i.short_desc)
        if self.weapon_wielding != self.default_weapon: 
            cons.write('You are wielding a %s.' % self.weapon_wielding.short_desc)
        if self.armor_worn != self.default_armor:
            cons.write('You are wearing a %s.' % self.armor_worn)
        return True
    
    def toggle_terse(self, p, cons, oDO, oIDO):
        try: 
            if p.words[1] == "on": 
                self.terse = True
            elif p.words[1] == "off": 
                self.terse = False
            else: 
                return """Usage: 'terse [on/off]'
                Use long descriptions (off) or short descriptions (on) when entering a place.
                With no specifier, 'terse' toggles between on and off."""
        except IndexError:
            self.terse = not self.terse
        cons.write("Terse mode %s. %s" % ("on" if self.terse else "off",
            "Short descriptions will be used when entering a place; type 'look' for full description" if self.terse else
            "Full descriptions will be used entering a place."))
        # TODO: a mode that prints long description only when first entering a room
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

    def fetch(self, p, cons, oDO, oIDO):
        '''Find an in-game object by ID and bring it to the player.'''
        if len(p.words) < 2: 
            cons.write("Usage: 'fetch <id>', where id is an entry in Thing.ID_dict[]")
            return True
        id = " ".join(p.words[1:])
        try:
            obj = Thing.ID_dict[id]
            if obj.move_to(self) == False:
                if obj.move_to(self.location) == False:
                    cons.write("You attempt to fetch the %s but somehow cannot bring it to this place." % obj.names[0])
                else:
                    cons.write("You perform a magical incantation and bring the %s to this place!" % obj.names[0])
            else:
                cons.write("You perform a magical incantation and the %s appears in your hands!" % obj.names[0])
            self.emit("%s performs a magical incantation, and you sense something has changed." % self.names[0], [self])
        except KeyError: 
            return "There seems to be no object with true name '%s'!" % id
        
        return True                    

    def clone(self, p, cons, oDO, oIDO):
        '''Clone a new copy of an object specified by ID or by module path, and bring it to the player.'''
        if len(p.words) < 2: 
            cons.write("Usage:\n\t'clone <id>', where id is an entry in Thing.ID_dict[]"
                       "\n\t'clone <path>', where path is of the form 'domains.school.test_object'")
            return True
        id = " ".join(p.words[1:])
        try:
            current_obj = Thing.ID_dict[id]
            objpath = current_obj.path
        except KeyError: 
            objpath = id
        obj = gametools.clone(objpath)
        if obj == None:
            return "There seems to be no object with true name '%s'!" % id
        if obj.move_to(self) == False:
            if obj.move_to(self.location) == False:
                cons.write("You attempt to clone the %s but somehow cannot bring it to this place." % obj.names[0])
            else:
                cons.write("You perform a magical incantation and bring the %s to this place!" % obj.names[0])
        else:
            cons.write("You perform a magical incantation and the %s appears in your hands!" % obj.names[0])
        self.emit("%s performs a magical incantation. You sense something has changed." % self.names[0], [self])
        
        return True                    

    
    def apparate(self, p, cons, oDO, oIDO):
        if len(p.words) < 2: 
            cons.write("Usage: 'apparate <id>', where id is the entry of a Room in Thing.ID_dict[] or a path to it's module")
            return True
        id = " ".join(p.words[1:])
        try:
            room = Thing.ID_dict[id]
        except KeyError: 
            room = gametools.load_room(id)
        if room == None:
            return "There seems to be no place with id (or path) '%s'!" % id
        if isinstance(room, Room) == False:
                cons.write("You cannot apparate to %s; that is not a place!" % room.names[0])
                return True
        self.emit("%s performs a magical incantation, and vanishes!" % self.names[0], [self])
        self.move_to(room)
        self.emit("%s arrives suddenly, as if by magic!" % self.names[0], [self])
        cons.write("You perform a magical incantation and are suddenly in a new place!")
        room.report_arrival(self)
        return True             

    
    def engage(self, p, cons, oDO, oIDO):
        if not oDO:
            return "Who do you intend to engage in combat?"
        self.attacking = oDO
        self.weapon_and_armor_grab()
        return True

    def disengage(self, p, cons, oDO, oIDO):        #TODO: Finish up.
        self.attacking = 'quit'
        return True

    def attack_enemy(self, enemy):
        if self.attacking in self.location.contents:
            self.attack(enemy)
        else:
            self.attacking = None