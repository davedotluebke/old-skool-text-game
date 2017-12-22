import thing
import action

def read(p, cons, oDO, oIDO):
    cons.write('You read:\nsometime in the next century. As has become clear, a more efficient, more logical system to organizing and structuring classes would be of great use to us. '
    'As for the purpouse itself, we shall see what the future holds and where things are going next. Therefore, I advise waiting before making the planned changes and hope to end the '
    'discussion on a good note you.\n\nSincerely,\nJavier Mons')
    return True

def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('paper', 'This paper appears to be part of a letter.')
    paper.actions.append(action.Action(read, ['read'], True, False))
    paper.add_names('letter')
    return paper
