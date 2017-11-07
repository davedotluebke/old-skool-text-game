from debug import dbg
from action import Action
from thing import Thing

class Armor(Thing):
    def __init__(self, default_name, path, bonus, unwieldiness, pref_id=None):
        Thing.__init__(self, default_name, path, pref_id)
        self.bonus = bonus
        self.unwieldiness = unwieldiness
        self.actions.append(Action(self.wear, ['wear','use'], True, False))
        self.actions.append(Action(self.unwear, ['unwear', 'remove'], True, False))
        # overwrite default drop action:
        for a in self.actions:
            if 'drop' in a.verblist:
                a.func = self.armor_drop

    def wear(self, p, cons, oDO, oIDO):
        if self == oDO:
            if self == cons.user.armor_worn:
                cons.write("You are already wearing the %s!" % self)
                return True
            if self.location != cons.user: 
                return "You need to be holding the %s to put it on." % self
            cons.user.armor_worn = self
            cons.write("You put on the %s." % self)
            cons.user.emit('&nD%s puts on the %s.' % (cons.user.id, self), ignore=[cons.user])
            return True
        else:
            return "Did you mean to wear a specific piece of armor, such as the %s?" % self

    def unwear(self, p, cons, oDO, oIDO):
        if self != oDO:
            return "Did you mean to take off a specific weapon, such as the %s?" % self
        if self != cons.user.armor_worn:
            return "But you aren't currently wearing the %s!" % self
        cons.user.armor_worn = cons.user.default_armor
        cons.write("You take off the %s." % self)
        cons.user.emit("&nD%s takes off the %s." % (cons.user.id, self), ignore=[cons.user])
        return True

    def armor_drop(self, p, cons, oDO, oIDO): 
        if self == oDO:
            if self == cons.user.armor_worn:
                cons.user.armor_worn = cons.user.default_armor
        return Thing.drop(self, p, cons, oDO, oIDO)