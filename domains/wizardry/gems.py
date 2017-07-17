# types of gems:
# [x] emerald - powers other gems
# [ ] jade - sends power from emerald long distances
# [x] ruby - makes light
# [x] dimond - makes things invisible
# [x] opal - makes dark
# [ ] saphire - allows people other than sky wizards to fly in nearby areas
# note that there are also other unique gems, such as the emerald of life, which have different powers than normal gems and are not listed here.

from thing import Thing
from player import Player
from action import Action

class Emerald(Thing):
    def __init__(self, default_name, short_desc, long_desc, power_num=10, pref_id=None):
        super().__init__(default_name, pref_id=None)
        self.set_description(short_desc, long_desc+' It is about %s milimeters in all dimentions.' % power_num)
        self.add_names('emerald')
        self.power_num = power_num
        self.actions.append(Action(self.move_power, ['power'], True, False))
    
    def power_gem(self, gem, amt):
        if amt > self.power_num:
            amt = self.power_num
        gem.power_num += amt
        self.power_num -= amt
        (head, sep, tail) = self.long_desc.partition(' It is about')
        self.long_desc = head + ' It is about %s milimeters in all dimentions.' % self.power_num
        if self.power_num <= 0:
            self.emit('The emerald shrinks and vanishes!')
            self.move_to(Thing.ID_dict['nulspace'])
    
    def move_power(self, p, cons, oDO, oIDO):
        if oDO == self and hasattr(oIDO, "power_num"):
            self.find_amount(cons, oIDO)
        elif oIDO == self and hasattr(oDO, 'power_num'):
            self.find_amount(cons, oDO)
        elif oIDO == None and oDO != self and hasattr(oDO, 'power_num'):
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

class Ruby(Thing):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, pref_id=None)
        self.set_description(short_desc, long_desc+' It almost seems to glow, as if light was trapped inside.')
        self.add_names('ruby')
        self.power_num = power_num
        self.light = 0
        Thing.ID_dict['nulspace'].game.register_heartbeat(self)

    def heartbeat(self):
        self.power_num = self.power_num - 1 if self.power_num > 1 else 0
        (head, sep, tail) = self.long_desc.partition(' It is ')
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
            
class Diamond(Thing):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, pref_id=None)
        self.set_description(short_desc, long_desc+' It is crystal clear.')
        self.add_names('diamond')
        self.power_num = power_num
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
        else:
            if self.hiding_user:
                self.user.invisible = False
                self.hiding_user = False
                self.user = None

class Opal(Thing):
    def __init__(self, default_name, short_desc, long_desc, power_num=0, pref_id=None):
        super().__init__(default_name, pref_id=None)
        self.set_description(short_desc, long_desc+' It is a swirl of colors that seem to draw light inside it.')
        self.add_names('opal')
        self.power_num = power_num
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
        