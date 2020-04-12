import thing
import action

#
# ACTION METHODS 
# 
def read(obj, p, cons, oDO, oIDO):
    cons.write('You read: Notice: I shall be out this week. Everything shall continue as normal.')
    return True

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('paper', 'This paper appears to be a note of some sort.')
    paper.add_names('note')
    # Add actions in clone() -> make a copy to not change Thing.actions[]
    paper.actions = dict(thing.Thing.actions)
    paper.actions['read'] = action.Action(read, True, False)
    return paper
