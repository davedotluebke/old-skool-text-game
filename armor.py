from debug import dbg
from action import Action
from thing import Thing

class Armor(Thing):
    def __init__(self, default_name, bonus, unwieldiness):
        Thing.__init__(self, default_name)
        self.bonus = bonus
        self.unwieldiness = unwieldiness