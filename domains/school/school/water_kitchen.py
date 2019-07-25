import gametools
import room
import scenery
import action
import liquid

class WaterJet(scenery.Scenery):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('jet', 'jet of water', 'This jet of water shoots from the rocks into the large pool in the center of the room.')
        self.unlisted = True
        self.add_adjectives('water')
        self.add_response(['drink'], 'You take a drink of the flowing water, and quench your thirst.', True, True)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def fill_container(self, p, cons, oDO, oIDO):
        if oDO == None: 
            return "What do you intend to fill from the jet of water?"
        
        filling = oDO
        if not getattr(filling, 'liquid'):
            cons.write('The water leaves the %s and flows into the pool.' % filling)
            return True
        cons.write('The water fills your %s' % filling)
        self.emit('&nD%s fills a %s with water from the jet.' % (cons.user.id, filling))
        water = gametools.clone('domains.school.school.water')
        oDO.insert(water)
        return True

    actions = dict(scenery.Scenery.actions)
    actions['fill'] = action.Action(fill_container, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    kitchen = room.Room('kitchen', roomPath, indoor=True, safe=True)
    kitchen.set_description('stone-walled kitchen', 'Stone walls surround a central pool in this kitchen,'
    ' with cabinets set into them. Jets of water squirt out of the walls, splashing into the pool.'
    ' A small door lies to the east.')
    kitchen.add_adjectives('stone-walled', 'water')
    kitchen.add_exit('down', 'domains.school.school.water_lounge')
    kitchen.add_exit('east', 'domains.school.school.office', caution_tape_msg="This door is locked.")

    jet_of_water = WaterJet()
    kitchen.insert(jet_of_water, True)

    cabinets = gametools.clone('domains.school.school.stone_cabinets')
    kitchen.insert(cabinets, True)
    return kitchen
