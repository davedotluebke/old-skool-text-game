import thing
import gametools
import action

class Match(thing.Thing):
    def __init__(self, default_name, path, pref_id=None, plural_name=None):
        super().__init__(default_name, path, pref_id=pref_id, plural_name=plural_name)
        self.flammable = 9

    def light_on_fire(self, p, cons, oDO, oIDO):
        if not oDO or oDO == self:
            return "Do you mean to light something on fire?"
        if oIDO and oIDO != self:
            return "Did you mean to light something on fire with the match?"
        if not oDO.flammable:
            cons.user.perceive("You try to light the %s on fire, but are unsuccesful." % oDO.name())
            return True
        if hasattr(oDO, 'burning') and oDO.burning:
            cons.user.perceive("The %s is already on fire!" % oDO)
            return True

        self.burning = True
        value = super().light_on_fire(p, cons, oDO, oIDO)
        if value != True:
            return value

        self.emit('The match is consumed by the fire.')
        self.destroy()
        return True
        
    actions = dict(thing.Thing.actions)
    actions['light'] = action.Action(light_on_fire, True, False)
    actions['burn'] = action.Action(light_on_fire, True, False)
    actions['ignite'] = action.Action(light_on_fire, True, False)

def clone():
    m = Match('match', __file__)
    m.set_description('ordinary match', 'This is an ordinary match.')
    m.add_adjectives('ordinary')
    return m