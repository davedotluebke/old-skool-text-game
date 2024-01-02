import gametools
import scenery
import room

class ClimbableBayWindow(scenery.Scenery):
    def __init__(self):
        super().__init__('window', 'bay window', 'This massive bay window looks out over the lawn. However, it\'s too dark inside to see in.', unlisted=True)
        self.add_adjectives('bay', 'massive')
        self.actions['climb'] = scenery.Action(ClimbableBayWindow.climb, True, False)

    def climb(self, p, cons, oDO, oIDO):
        if oDO != self and oIDO != self:
            return "Did you mean to climb through the window?"
        
        ladder_in_room = False

        for i in self.location.contents:
            if i.path == 'domains.centrata.mansion.ladder':
                ladder_in_room = True
                break
        
        if not ladder_in_room:
            cons.user.perceive("The window seems too high to climb through, just out of reach.")
            return True

        cons.user.perceive("You climb up the ladder and through the window.")
        self.emit("&nD%s climbs the ladder and through the window." % cons.user, ignore=[cons.user])
        cons.user.move_to(gametools.load_room('domains.centrata.mansion.office'))
        return True

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('lawn', roomPath)
    r.set_description('east lawn', 'You stand outside the mansion on the east side.')
    r.add_exit('northwest', 'domains.centrata.mansion.gate_inside')
    r.add_exit('southwest', 'domains.centrata.mansion.south_lawn')

    mansion_scenery_east = scenery.Scenery('mansion', 'sandstone mansion', 'A massive bay window looks out onto the lawn. A wing stretches out to the south.', unlisted=True)
    mansion_scenery_east.add_adjectives('sandstone', 'massive')
    r.insert(mansion_scenery_east, True)

    bay_window_scenery = ClimbableBayWindow()
    r.insert(bay_window_scenery, True)

    return r
