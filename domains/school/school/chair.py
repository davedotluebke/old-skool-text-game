import thing
import random
import action
import gameserver

class Chair(thing.Thing):
    availible_colors = ['red', 'orange', 'brown', 'maroon', 'gold']
    in_chairs = []
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, color):
        super().__init__('chair', __file__)
        self.set_description('%s chair' % color, 'This comfortable chair is covered in a %s felt-like surface.' % color)
        del Chair.availible_colors[Chair.availible_colors.index(color)]
        self.add_adjectives('comfortable',color)
        self.sitting = None
        self.color = color
        thing.Thing.game.register_heartbeat(self)

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        if self.sitting == None:
            return
        if self.sitting.location != self.location:
            self.sitting = None

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def sit(self, p, cons, oDO, oIDO):
        if self.sitting == cons.user:
            cons.user.perceive("You are already sitting in the chair!")
            return True
        if self.sitting != None:
            return "The chair is occupied!"
        if cons.user in Chair.in_chairs:
            return "You are already sitting in a different chair!"
        self.sitting = cons.user
        self.emit("&nd%s sits down in the %s chair." % (cons.user, self.color), ignore=[cons.user])
        cons.user.perceive("You sit down in the %s chair and relax." % self.color)
        Chair.in_chairs.append(cons.user)
        return True

    def stand(self, p, cons, oDO, oIDO):
        if self.sitting != cons.user:
            return "You aren't sitting in the chair!"
        self.sitting = None
        self.emit("&nd%s stands up from the %s chair" % (cons.user, self.color), ignore=[cons.user])
        cons.user.perceive("You stand up from the %s chair." % self.color)
        del Chair.in_chairs[Chair.in_chairs.index(cons.user)]
        return True
        
    actions = dict(thing.Thing.actions)
    actions['sit'] =    Action(sit, True, True)
    actions['relax'] =  Action(sit, True, True)
    actions['stand'] =  Action(sit, False, True)
    
def clone():
    try:
        color = random.choice(Chair.availible_colors)
    except IndexError:
        Chair.availible_colors = ['red', 'orange', 'brown', 'maroon', 'gold']
        color = random.choice(Chair.availible_colors)
    return Chair(color)
