import thing
import action

def read(p, cons, oDO, oIDO):
    cons.write('You read: Make sure to check in on anouncements. Make clear importance of exploration.')
    return True

def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('paper', 'This paper appears to be a note of some sort.')
    paper.actions.append(action.Action(read, ['read'], True, False))
    paper.add_names('note')
    return paper
