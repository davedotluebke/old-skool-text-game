from debug import dbg
from action import Action
from thing import Thing

class Armor(Thing):
    def __init__(self, default_name, damage_prevent_num, unweildiness):
        Thing.__init__(self, default_name)
        self.damage_prevent_num = damage_prevent_num
        self.unweildiness = unweildiness