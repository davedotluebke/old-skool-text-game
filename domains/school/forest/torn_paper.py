import thing
import action

#
# ACTION METHODS 
# 
def read(obj, p, cons, oDO, oIDO):
    cons.write('''All you can make out from the paper is a poem that says:
    Sometimes
    It is a trick
    That will set you free.''')
    return True

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('torn paper', 'This paper appears to be torn from a book.')
    paper.add_adjectives('torn')
    # Add actions in clone() -> make a copy to not change Thing.actions[]
    paper.actions = dict(thing.Thing.actions)
    paper.actions['read'] = action.Action(read, True, False)
    return paper
