import container
import weapon
import gametools

class Oyster(container.Container):
    def __init__(self):
        super().__init__('oyster', __file__)
        self.set_description('ordinary oyster', 'This is an ordinary oyster. It seems firmly closed, but you almost think you see a pearl inside.')
        self.closable = True
        self.actions.append(container.Action(self.open, ['open', 'separate'], True, False))
        self.insert(gametools.clone('domains.school.elementQuest.pearl'))
        
    def open(self, p, cons, oDO, oIDO):
        if isinstance(oIDO, weapon.Weapon):
            return super().open(p, cons, oDO, oIDO)
        else:
            cons.user.perceive("You can't open the oyster without using some sort of tool.")
            return True

def clone():
    return Oyster()