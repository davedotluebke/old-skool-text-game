from debug import dbg
from thing import Thing
from scenery import Scenery
from action import Action
from liquid import Liquid

class Sink(Thing):
    def __init__(self, ID):
        Thing.__init__(self, ID)
        self.set_description('metal sink', 'This is an old metal sink, probably from the 1960s and nothing seems wrong with it.')
        self.fix_in_place("You can't take the sink!")
        self.actions.append(Action(self.fill_container, ["fill"], True, False))
    
    def fill_container(self, p, cons, oDO, oIDO):
        if oDO == None: 
            return "What do you intend to fill from the sink?"
        
        filling = oDO
        cons.write('Water comes out of the sink, and fills your %s' % filling)
        self.emit('The %s is filled with water at the sink.' % filling)
        water = Liquid('water', 'some normal water', 'This is some normal clear water.')
        water.add_response(['drink'], 'You take a big drink of the water, and your thirst is quenched.')
        oDO.insert(water)
        return True