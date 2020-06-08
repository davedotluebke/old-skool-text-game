from stones import *

# this file is maintained for backwards compatibility. See stones.py for the newer syntax
class Gem(Stone):
    def __init__(self, path, default_name, short_desc, long_desc, power_num=10, pref_id=None):
        super().__init__(default_name, path, mana=power_num, max_mana=power_num)
        self.set_description(short_desc, long_desc)
        self.log.warning('This is deprecated. Use stones.Stone instead.')

Emerald = Gem
Ruby = Gem
Jade = Gem
Diamond = Gem
Opal = Gem
Pearl = Gem

"""Old gem system is below for now.
# types of gems:
# [x] emerald - powers other gems
# [x] jade - sends power from emerald long distances
# [x] ruby - makes light
# [x] dimond - makes things invisible
# [x] opal - makes dark
# [ ] saphire - allows people to fly in nearby areas (hardcode rooms that people can fly in, rather than giving the immobile saphires any power)
# [x] pearl - tones down the power from an emerald, but makes it last longer
# note that there are also other unique gems, such as the emerald of life, which have different powers than normal gems and are not listed here.

import random
import copy

from thing import Thing
from container import Container
from player import Player
from action import Action
# Gem is a generic base class for all gems, used for isinstance() and other internal functions.
class Gem(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, path, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.power_num = power_num
        self.set_description(short_desc, long_desc)

class Emerald(Gem):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, path, default_name, short_desc, long_desc, power_num=10, pref_id=None):
        super().__init__(path, default_name, short_desc, long_desc+' It is about %s millimeters in all dimensions.' % power_num, power_num, pref_id)
        self.add_names('emerald')
        self.next_power = None
        self.cons = None
    
    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #
    def _adjust_description(self):
        (head, sep, tail) = self._long_desc.partition(' It is about')
        self._long_desc = head + ' It is about %s millimeters in all dimensions.' % self.power_num
        if self.power_num <= 0:
            self.emit('The emerald shrinks and vanishes!')
            self.destroy()
    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def power_gem(self, gem, amt):
        if amt > self.power_num:
            amt = self.power_num
        gem.power_num += amt
        self.power_num -= amt
        self._adjust_description()
    
    def find_amount(self, cons, gem):
        cons.write('How much power would you like to move? Type it below:')
        cons.request_input(self)
        self.next_power = gem
        self.cons = cons

    def console_recv(self, amt):
        try:
            amt = int(amt)
        except:
            amt = 1
        self.power_gem(self.next_power, amt)
        self.cons.write("You feel the power moving from the emerald to the %s." % self.next_power._short_desc)
        self.cons.input_redirect = None
        self.next_power = None
        self.cons = None
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #   
    def move_power(self, p, cons, oDO, oIDO):
        if oDO == self and isinstance(oIDO, Gem):
            self.find_amount(cons, oIDO)
        elif oIDO == self and isinstance(oDO, Gem):
            self.find_amount(cons, oDO)
        elif oIDO == None and oDO != self and isinstance(oDO, Gem):
            self.find_amount(cons, oDO)
        elif oIDO == None and oDO == self:
            return "Did you mean to put power into the emerald?"
        else:
            return "I don't quite understand what you meant."
        return True
        
    actions = dict(Gem.actions)
    actions['power'] = Action(move_power, True, False)

class Jade(Gem):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, path, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(path, default_name, short_desc, long_desc+' It seems almost as if it were somewhere else.', power_num, pref_id)
        self.add_names('jade')
        Thing.game.register_heartbeat(self)
        self.cons = None

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        if self.power_num > 0:
            possible_players = [x for x in self.location.contents]
            possible_players.append(self.location)
            for i in possible_players:
                if isinstance(i, Player):
                    i.cons.write('Where would you like to send this power? Type the true name of the place you want to send the power below:')
                    i.cons.request_input(self)
                    self.cons = self
                    return
            loc = random.choice(Thing.ID_dict)
            self.send_power(loc)

    def console_recv(self, message):
        try:
            self.send_power(Thing.ID_dict[message])
        except:
            loc = random.choice(Thing.ID_dict)
            self.send_power(loc)
        self.cons.input_redirect = None
        self.cons = None
    
    def send_power(self, loc):
        if not loc.contents:
            loc = random.choice([x for x in Thing.ID_dict if isinstance(x, Container)])
        objs = copy.deepcopy(loc.contents)
        while self.power_num > 0:
            obj = random.choice(objs)
            if isinstance(obj, Gem):
                obj.power_num += 1
                self.power_num -= 1
                if isinstance(obj, Emerald):
                    obj._adjust_description()
            if isinstance(obj, Container):
                objs.append(obj.contents)
            del objs[objs.index(obj)]
            if not objs:
                break

class Ruby(Gem):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, path, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(path, default_name, short_desc, long_desc+' It almost seems to glow, as if light was trapped inside.', power_num, pref_id)
        self.add_names('ruby')
        self.light = 0
        Thing.game.register_heartbeat(self)

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        self.power_num = self.power_num - 1 if self.power_num > 1 else 0
        (head, sep, tail) = self._long_desc.partition(' It ')
        if self.power_num >= 10:
            self._long_desc = head + ' It is brilliantly glowing red.'
            self.light = 2
        elif self.power_num >= 5:
            self._long_desc = head + ' It is brightly glowing red.'
            self.light = 1
        elif self.power_num >= 2:
            self._long_desc = head + ' It is faintly glowing red.'
            self.light = 0
        else:
            self._long_desc = head + ' It almost seems to glow, as if light was trapped inside.'
            
class Diamond(Gem):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, path, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(path, default_name, short_desc, long_desc+' It is crystal clear.', power_num, pref_id)
        self.add_names('diamond')
        self.hiding_user = False
        self.user = None
        Thing.game.register_heartbeat(self)

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        if self.power_num > 0:
            self.power_num -= 1
            if not self.hiding_user:
                if isinstance(self.location, Player):
                    self.location.invisible = True
                    self.user = self.location
                    self.hiding_user = True
                    self.user.cons.write("You notice yourself fading. ")
                    self.user.emit("&nD%s suddenly disappears!" % self.user.id, ignore=[self.user])
        else:
            if self.hiding_user:
                self.user.invisible = False
                self.user.cons.write("You notice yourself fading back into visibility.")
                self.user.emit("&nI%s suddenly appears!" % self.user.id, ignore=[self.user])
                self.hiding_user = False
                self.user = None

class Opal(Gem):
    def __init__(self, path, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(path, default_name, short_desc, long_desc+' It is a swirl of colours that seem to draw light inside it.', power_num, pref_id=None)
        self.add_names('opal')
        self.light = 0  # light is negative if powered, 0 otherwise (default 0)
        Thing.game.register_heartbeat(self)

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        self.power_num = self.power_num - 1 if self.power_num > 1 else 0
        (head, sep, tail) = self._long_desc.partition(' It ')
        if self.power_num >= 5:
            self._long_desc = head + ' It is a swirl of colours, spinning and pulling the light into it.'
            self.light = -1
        elif self.power_num >= 2:
            self._long_desc = head + ' It seems like the surrounding light is going behind the swirl, trapped.'
            self.light = 0
        else:
            self._long_desc = head + ' It is a swirl of colours that seem to draw light inside it.'

class Pearl(Gem):
    def __init__(self, path, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(path, default_name, short_desc, long_desc+' It almosts looks as if it is reflecting you, but softer.')
        self.add_names('pearl')
        self.alternator_subtract = False
        self.powering = None
        Thing.game.register_heartbeat(self)
    
    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        if not self.powering:
            if self.power_num > 0:
                if self.alternator_subtract == True:
                    self.power_num -= 1
                    self.alternator_subtract = False
                else:
                    self.alternator_subtract = True
            return
        if self.alternator_subtract == True:
            self.power_gem(self.powering)
            self.alternator_subtract = False
        else:
            self.alternator_subtract = True
        
    def power_gem(self, gem):
        gem.power_num += 1
        self.power_num -= 1

    def move_power(self, gem):
        self.powering = gem

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def move_power(self, p, cons, oDO, oIDO):
        if oDO == self and isinstance(oIDO, Gem):
            self.move_power(oIDO)
        elif oIDO == self and isinstance(oDO, Gem):
            self.move_power(oDO)
        elif oIDO == None and oDO != self and isinstance(oDO, Gem):
            self.move_power(oDO)
        elif oIDO == None and oDO == self:
            return "Did you mean to put power into the pearl?"
        else:
            return "I don't quite understand what you meant."
        return True
"""