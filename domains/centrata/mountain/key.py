import thing
import action

class Key(thing.Thing):
    def take(self, p, cons, oDO, oIDO):
        """An override of the take function to add the functionality of angering the Quavari."""
        confirmed = super().take(p, cons, oDO, oIDO)
        if confirmed:
            self.quavari.enemies.append(cons.user)
        return confirmed
    
    actions = dict(thing.Thing.actions)
    actions['take'] = action.Action(take, True, False)
    actions['get'] = action.Action(take, True, False)

def clone():
    key = Key('key', __file__)
    key.set_description('shiny golden key', 'This is a shiny golden key.')
    key.add_adjectives('shiny', 'golden')
    return key
