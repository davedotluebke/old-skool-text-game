import room
import gametools
import scenery
import action

class AirPortal(scenery.Scenery):
    def __init__(self):
        super().__init__('portal', 'misty portal', 'This is a strange misty portal beside the mountain. It is swirling rapidly.', unlisted=True)
        self.add_adjectives('misty', 'swirling', 'rapidly')
        self.actions['enter'] = action.Action(self.enter, True, False)
    
    def enter(self, p, cons, oDO, oIDO):
        cons.user.wizardry_element = 'air'
        cons.user.complete_quest('Complete a quest to find thy element')
        cons.user.perceive('As you step into the misty portal, you begin to feel the swirling winds pushing against you. '
                           'Somehow, however, it doesn\'t seem unconfortable. Then, all of the sudden, '
                           'you begin to feel as if you have given in to--no, '
                           'ABSORBED the winds. You suddenly realize you are in a different place...')
        lounge = gametools.load_room('domains.school.school.air_lounge')
        if lounge and cons.user.move_to(lounge):
            self.emit('&nD%s steps into the misty portal and slowly vanishes.' % cons.user)
        else:
            cons.user.perceive('...and just as quickly, you feel yourself return! But something has changed...')
        return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('ledge', roomPath)
    r.set_description('mountainside ledge', 'You stand on a small ledge beside a mountain, overlooking a great chasm below. '
    'To the east a stone bridge with a rainbow projected on it leads over the chasm to a tower. To the north you see a misty portal, swirling rapidly. ')
    r.add_exit('east', 'domains.school.elementQuest.bridge')

    portal = AirPortal()
    r.insert(portal)

    return r
