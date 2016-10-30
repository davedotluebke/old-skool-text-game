from thing import Thing
from scenery import Scenery
from debug import dbg
class Sink(Thing):
    def __init__(self, ID):
        Thing.__init__(self, ID)
        self.set_description('a metal sink', 'This is an old metal sink, probably from the 1960s and nothing seems wrong with it.')
        self.fix_in_place("You can't take the sink!")
        self.add_verb('fill', self.fill_container)
    
    def fill_container(self, p, cons, oDO, oIDO):
        filling = '%s' % p.words[1]
        cons.write('Water comes out of the sink, and fills your %s' % filling)
        self.emit('The %s is filled with water at the sink.' % filling)
        self.water = Scenery('water', 'some normal water', 'This is some normal clear water.',[('drink', 'You take a big drink of the water, and your thirst is quenched.')])
        exec_string = '%s.insert(self.water)'
        exec(exec_string)