from debug import dbg
from action import Action
from thing import Thing

class Armor(Thing):
    def __init__(self, default_name, bonus, unwieldiness, pref_id=None):
        Thing.__init__(self, default_name, pref_id)
        self.bonus = bonus
        self.unwieldiness = unwieldiness