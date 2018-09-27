from debug import dbg
from action import Action
from thing import Thing

class Weapon(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, damage, accuracy, unwieldiness, attack_verbs=['swing'], pref_id=None):
        Thing.__init__(self, default_name, path, pref_id)
        self.damage = damage
        self.accuracy = accuracy
        self.unwieldiness = unwieldiness
        self.actions = dict(Thing.actions)
        self.actions['wield'] =   Action(self.wield, True, False)
        self.actions['use'] =     Action(self.wield, True, False)
        self.actions['unwield'] = Action(self.unwield, True, False)
        for i in attack_verbs:
            self.actions[i] = Action(self.start_attack, True, False)
        # overwrite default drop action:
        self.actions['drop'] = Action(self.weapon_drop, True, False)

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    #
    # SET/GET METHODS (methods to set or query attributes)
    #

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #

    def wield(self, p, cons, oDO, oIDO):
        if self == oDO:
            if self == cons.user.weapon_wielding:
                cons.write("You are already wielding the %s!" % self)
                return True
            if self.location != cons.user: 
                return "You need to be holding the %s to wield it." % self
            cons.user.weapon_wielding = self
            cons.write("You wield the %s." % self)
            cons.user.emit('&nD%s wields the %s.' % (cons.user, self), ignore=[cons.user])
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
        cons.user.emit("&nD%s puts away the %s." % (cons.user, self), ignore=[cons.user])
        return True

    def weapon_drop(self, p, cons, oDO, oIDO): 
        if self == oDO:
            if self == cons.user.weapon_wielding:
                cons.user.weapon_wielding = cons.user.default_weapon
        return Thing.drop(self, p, cons, oDO, oIDO)

    def start_attack(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if cons.user.weapon_wielding != self:
            cons.user.weapon_wielding = self
            cons.user.perceive("You wield the %s." % self.names[0])
        if not oDO or not oIDO:
            return "Try specifying a weapon and target, such as %s %s at [target]." % (sV, self.names[0])
        if oDO == self:
            if cons.user.attacking != None:
                cons.user.perceive('You switch your attack to &nd%s.' % oIDO)
            else:
                cons.user.perceive('You %s the %s at &nd%s.' % (sV, self, oIDO))
            cons.user.attacking = oIDO
            return True
        elif oIDO == self:
            if cons.user.attacking != None and cons.user.attacking != 'quit':
                cons.user.perceive('You switch your attack to &nd%s.' % oIDO)
                cons.user.attacking = oIDO
            else:
                cons.user.perceive('You %s &nd%s with the %s.' % (sV, oIDO, self))
            return True

        return "Did you mean to %s the %s?" % (sV, self.get_short_desc())

#
# MODULE-LEVEL FUNCTIONS (e.g., clone())
#
