from debug import dbg
from action import Action
from thing import Thing

class Weapon(Thing):
    def __init__(self, default_name, damage, accuracy, unwieldiness, pref_id=None):
        Thing.__init__(self, default_name, pref_id)
        self.damage = damage
        self.accuracy = accuracy
        self.unwieldiness = unwieldiness