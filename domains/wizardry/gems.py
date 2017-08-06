# types of gems:
# [x] emerald - powers other gems
# [ ] jade - sends power from emerald long distances
# [x] ruby - makes light
# [x] dimond - makes things invisible
# [x] opal - makes dark
# [ ] saphire - allows people other than sky wizards to fly in nearby areas
# note that there are also other unique gems, such as the emerald of life, which have different powers than normal gems and are not listed here.

import random
import copy

from thing import Thing
from container import Container
from player import Player
from action import Action
# Gem is a generic base class for all gems, used for isinstance() and other internal functions.
class Gem(Thing):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, pref_id)
        self.power_num = power_num
        self.set_description(short_desc, long_desc)

class Emerald(Gem):
    def __init__(self, default_name, short_desc, long_desc, power_num=10, pref_id=None):
        super().__init__(default_name, short_desc, long_desc+' It is about %s milimeters in all dimentions.' % power_num, power_num, pref_id)
        self.add_names('emerald')
        self.actions.append(Action(self.move_power, ['power'], True, False))
    
    def power_gem(self, gem, amt):
        if amt > self.power_num:
            amt = self.power_num
        gem.power_num += amt
        self.power_num -= amt
        self.adjust_description()

    def adjust_description(self):
        (head, sep, tail) = self.long_desc.partition(' It is about')
        self.long_desc = head + ' It is about %s milimeters in all dimentions.' % self.power_num
        if self.power_num <= 0:
            self.emit('The emerald shrinks and vanishes!')
            self.move_to(Thing.ID_dict['nulspace'])
    
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
    
    def find_amount(self, cons, gem):
        cons.write('How much power would you like to move? Type it below:')
        amt = cons.take_input('-> ') #XXX replace with symilar system that will work in multiplayer
        try:
            amt = int(amt)
        except ValueError:
            cons.parser.parse(cons.user, cons, amt)
            return
        self.power_gem(gem, amt)
        cons.write("You feel the power moving from the emerald to the %s." % gem.short_desc)

class Jade(Gem):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, short_desc, long_desc+' It seems as almost as if it were somewhere else.', power_num, pref_id)
        self.add_names('jade')
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)

    def heartbeat(self):
        if self.power_num > 0:
            possible_players = [x for x in self.location.contents]
            possible_players.append(self.location)
            for i in possible_players:
                if isinstance(i, Player):
                    i.cons.write('Where would you like to send this power? Type the true name of the place you want to send the power below:')
                    sLoc = i.cons.take_input('-> ')
                    try:
                        loc = Thing.ID_dict[sLoc]
                    except KeyError:
                        i.cons.parser.parse(sLoc)
                        return
                    self.send_power(loc)
                    return
            loc = random.choice(Thing.ID_dict)
            self.send_power(loc)
    
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
                    obj.adjust_description()
            if isinstance(obj, Container):
                objs.append(obj.contents)
            del objs[objs.index(obj)]
            if not objs:
                break

class Ruby(Gem):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, short_desc, long_desc+' It almost seems to glow, as if light was trapped inside.', power_num, pref_id)
        self.add_names('ruby')
        self.light = 0
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)

    def heartbeat(self):
        self.power_num = self.power_num - 1 if self.power_num > 1 else 0
        (head, sep, tail) = self.long_desc.partition(' It ')
        if self.power_num >= 10:
            self.long_desc = head + ' It is briliantly glowing red.'
            self.light = 2
        elif self.power_num >= 5:
            self.long_desc = head + ' It is brightly glowing red.'
            self.light = 1
        elif self.power_num >= 2:
            self.long_desc = head + ' It is faintly glowing red.'
            self.light = 0
        else:
            self.long_desc = head + ' It almost seems to glow, as if light was trapped inside.'
            
class Diamond(Gem):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, short_desc, long_desc+' It is crystal clear.', power_num, pref_id)
        self.add_names('diamond')
        self.hiding_user = False
        self.user = None
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)

    def heartbeat(self):
        if self.power_num > 0:
            self.power_num -= 1
            if not self.hiding_user:
                if isinstance(self.location, Player):
                    self.location.invisible = True
                    self.user = self.location
                    self.hiding_user = True
                    self.user.cons.write("You notice yourself fading. ")
                    self.user.emit("%s suddenly dissapears!" % self.user, ignore=[self.user])
        else:
            if self.hiding_user:
                self.user.invisible = False
                self.user.cons.write("You notice yourself fading back into visibility.")
                self.user.emit("%s suddenly appears!" % self.user, ignore=[self.user])
                self.hiding_user = False
                self.user = None

class Opal(Gem):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, short_desc, long_desc+' It is a swirl of colors that seem to draw light inside it.', power_num, pref_id=None)
        self.add_names('opal')
        self.light = 0  # light is negative if powered, 0 otherwise (default 0)
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)

    def heartbeat(self):
        self.power_num = self.power_num - 1 if self.power_num > 1 else 0
        (head, sep, tail) = self.long_desc.partition(' It ')
        if self.power_num >= 5:
            self.long_desc = head + ' It is a swirl of colors, spinning and pulling the light into it.'
            self.light = -1
        elif self.power_num >= 2:
            self.long_desc = head + ' It seems like the surrouning light is going behind the swirl, trapped.'
            self.light = 0
        else:
            self.long_desc = head + ' It is a swirl of colors that seem to draw light inside it.'
        