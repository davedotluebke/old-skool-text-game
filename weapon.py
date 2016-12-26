from debug import dbg
from action import Action
from thing import Thing

class Weapon(Thing):
    def __init__(self, default_name, damage, accuracy, unwieldiness):
        Thing.__init__(self, default_name)
        self.damage = damage
        self.accuracy = accuracy
        self.unwieldiness = unwieldiness