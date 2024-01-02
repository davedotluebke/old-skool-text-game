import thing
import action

class Pen(thing.Thing):
    def __init__(self):
        super().__init__('pen', __file__)
        self.set_description('black pen', 'This is a black pen.')
        self.add_adjectives('black')

    def write(self, p, cons, oDO, oIDO):
        if not oIDO:
            return "Did you mean to write on something?"

        if not hasattr(oIDO, 'accepts_writing') or not oIDO.accepts_writing:
            cons.user.perceive(f"The {oIDO.names[0]} isn't intended to be written on.")
            return True

        sV, sDO, sPrep, sIDO = p.diagram_sentence(p.words)

        if not sDO:
            return f"Did you mean to write something on the {oIDO.names[0]}?"
        
        if self not in cons.user.contents:
            cons.user.perceive("You must be holding the pen to write with it.")
            return True

        if f'On the {oIDO.names[0]} the following is written:' not in oIDO._long_desc:
            oIDO._long_desc += f'\n\nOn the {oIDO.names[0]} the following is written:\n\n'

        oIDO._long_desc += '\n' + sDO
        cons.user.perceive(f'You write {sDO} on the {oIDO.names[0]}.')
        return True

    actions = dict(thing.Thing.actions)
    actions['write'] = action.Action(write, True, True)

def clone():
    return Pen()
