import thing
import action

class Scroll(thing.Thing):
    #
    # Special Object Methods (e.g. __init__)
    #
    def __init__(self):
        super().__init__('scroll', __file__)
        self.set_description('scroll', 'You shouln\'t ever see this message, if you do please "read" the scroll and report a bug.')
    
    #
    # Special Methods (_method(), not imported)
    #

    #
    # Other miscelaneous methods
    #

    def move_to(self, dest, force_move=False, merge_pluralities=True):
        value = super().move_to(dest, force_move=force_move, merge_pluralities=merge_pluralities)
        self.emit('The scroll glows for a second!')
        return value
    
    #
    # Action methods and dictionary (methods come first)
    #
    def read(self, p, cons, oDO, oIDO):
        if self == oDO or self == oIDO:
            if cons.user != self.location:
                cons.user.perceive("The scroll is mysteriously blank.")
                return True
            
            msg = "On this scroll you read:\n\n"
            for i in self.location.quest_list:
                if i[1] == True: # quest is complete
                    msg += f"~~{i[0]}~~\n" # XXX strikethrough not working right now
                else:
                    msg += i[0] + '\n'
            
            cons.user.perceive(msg)
            return True
        else:
            return "Not sure what you are trying to look at!"
    
    actions = dict(thing.Thing.actions)
    actions['read'] = action.Action(read, True, False)
    actions['look'] = action.Action(read, True, False)

#
# Module level functions (e.g. clone, load)
#

def clone(player_obj=None):
    return Scroll()
