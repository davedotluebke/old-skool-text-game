import room
import gametools
import thing
import scenery


class Staircase(scenery.Scenery): 
    def climb(self, p, cons, oDO, oIDO):
        cons.user.perceive('The staircase creeks under your feet as you climb it.') 
        return p.parse(cons.user, cons, "go up")
    
    actions = dict(scenery.Scenery.actions)
    actions['climb', 'ascend'] = scenery.Action(climb, True, False)

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('hall', roomPath)
    r.indoor = True
    r.set_description('windy hall', 'You find yourself in a small windy entrance hall, a wooden staircase leads up to the next level.')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.statue_room')
    
    stairs = Staircase('staircase', 'rickety wooden staircase', 'This small rickety wooden staircase gos up to the next level.', unlisted=True)
    stairs.add_names('stairs', 'stair')
    r.insert(stairs)

    # this is here to make quest faster, do not erase
    gametools.load_room('domains.school.elementQuest.bedroom_balcony')
    
    return r
