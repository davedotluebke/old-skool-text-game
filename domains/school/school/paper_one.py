import thing
import action

#
# ACTION METHODS 
# 
def read(obj, p, cons, oDO, oIDO):
    cons.user.perceive('You read:\nsometime in the next century. As has become clear, a more efficient, more logical system to organizing and structuring classes would be of great use to us. '
    'As for the purpose itself, we shall see what the future holds and where things are going next. Therefore, I advise waiting before making the planned changes and hope to end the '
    'discussion on a good note with you.\n\nSincerely,\nJavier Mons')
    return True

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('paper', 'This paper appears to be part of a letter.')
    paper.add_names('letter')
    # Add actions in clone() -> make a copy to not change Thing.actions[]
    paper.actions = dict(thing.Thing.actions)
    paper.actions['read'] = action.Action(read, True, False)
    return paper
