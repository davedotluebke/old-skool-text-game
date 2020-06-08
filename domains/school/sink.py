import gametools

from thing import Thing
from scenery import Scenery
from action import Action
from liquid import Liquid

class Sink(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, ID, path):
        Thing.__init__(self, ID, path)
        self.set_description('metal sink', "This is an old metal sink, probably from the 1960's, and nothing seems wrong with it.")
        self.fix_in_place("You can't take the sink!")
    
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def fill_container(self, p, cons, oDO, oIDO):
        if oDO == None: 
            return "What do you intend to fill from the sink?"
        
        filling = oDO
        if not getattr(filling, 'liquid'):
            cons.write('The water leaves the %s and goes down the drain in the sink' % filling)
            return True
        cons.write('Water comes out of the sink, and fills your %s' % filling)
        self.emit('&nD%s fills a %s with water at the sink.' % (cons.user.id, filling))
        water = gametools.clone('domains.school.school.water')
        oDO.insert(water)
        return True
    
    def pour_out_in_sink(self, p, cons, oDO, oIDO):
        if oDO:
            obj = oDO
        else:
            obj = oIDO
        if obj == self or obj == None:
            return "It is impossible to pour out a sink in a sink."
        cons.write('You pour the %s into the sink, and it goes down the drain.' % obj)
        self.emit("&nD%s pours something into the sink." % cons.user.id)
        obj.destroy()
        return True
        #TODO: Actually delete the object

    actions = dict(Thing.actions)
    actions['fill'] = Action(fill_container, True, False)
    actions['pour'] = Action(pour_out_in_sink, True, False)