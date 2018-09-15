import container
import weapon
import gametools

class Oyster(container.Container):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('oyster', __file__)
        self.set_description('ordinary oyster', 'This is an ordinary oyster. It seems firmly closed, but you almost think you see a pearl inside.')
        self.closable = True
        self.close()
        self.insert(gametools.clone('domains.school.elementQuest.pearl'))
    
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #      
    def open(self, p, cons, oDO, oIDO):
        if isinstance(oIDO, weapon.Weapon):
            return super().open(p, cons, oDO, oIDO)
        else:
            cons.user.perceive("You can't open the oyster without using some sort of tool.")
            return True
    actions  = dict(Container.actions)  # make a copy
    actions['open'] =     Action(open, True, False)
    actions['pry'] =      Action(open, True, False)
    actions['separate'] = Action(open, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    return Oyster()