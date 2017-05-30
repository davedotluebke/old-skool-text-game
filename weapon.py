from debug import dbg
from action import Action
from thing import Thing

class Weapon(Thing):
    def __init__(self, default_name, damage, accuracy, unwieldiness, pref_id=None):
        Thing.__init__(self, default_name, pref_id)
        self.damage = damage
        self.accuracy = accuracy
        self.unwieldiness = unwieldiness
        self.actions.append(Action(self.wield, ['wield', 'use'], True, False))
        self.actions.append(Action(self.unwield, ['unwield'], True, False))
        # overwrite default drop action:
        for a in self.actions:
            if 'drop' in a.verblist:
                a.func = self.weapon_drop
        
    def wield(self, p, cons, oDO, oIDO):
        if self == oDO:
            if self == cons.user.weapon_wielding:
                cons.write("You are already wielding the %s!" % self)
                return True
            if self.location != cons.user: 
                return "You need to be holding the %s to wield it." % self
            cons.user.weapon_wielding = self
            cons.write("You wield the %s." % self)
            cons.user.emit('%s wields the %s.' % (cons.user, self), ignore=[cons.user])
            return True
        else:
            return "Did you mean to wield a specific weapon, such as the %s?" % self

    def unwield(self, p, cons, oDO, oIDO):
        if self != oDO:
            return "Did you mean to unwield a specific weapon, such as the %s?" % self
        if self != cons.user.weapon_wielding:
            return "But you aren't currently wielding the %s!" % self
        cons.user.weapon_wielding = cons.user.default_weapon
        cons.write("You cease wielding the %s." % self)
        cons.user.emit("%s puts away the %s." % (cons.user, self), ignore=[cons.user])
        return True

    def weapon_drop(self, p, cons, oDO, oIDO): 
        if self == oDO:
            if self == cons.user.weapon_wielding:
                cons.user.weapon_wielding = cons.user.default_weapon
        return Thing.drop(self, p, cons, oDO, oIDO)

