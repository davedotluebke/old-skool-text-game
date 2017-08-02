import thing
import action

def read(p, cons, oDO, oIDO):
    cons.write('''All you can make out from the paper is a poem that says:
    Sometimes
    It is a trick
    That will set you free.''')
    return True

def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('torn paper', 'This paper appears to be torn from a book.')
    paper.actions.append(action.Action(read, ['read'], True, False))
    paper.add_adjectives('torn')
    return paper
