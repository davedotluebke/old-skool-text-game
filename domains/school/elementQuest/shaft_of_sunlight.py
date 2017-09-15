import room
import gametools
import thing
import scenery
import container

class Shaft(thing.Thing):
    def hold(self, p, cons, oDO, oIDO):
    # Idea: for any object held in the shaft of sunlight, test if it is a see-through container holding 
    # "liquid fire" potion. If so, the potion alights!
    # Should work for 'hold x in shaft', 'wave x in shaft of sunlight', 'wave x through shaft', etc. 
        pass


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('sunlit room', roomPath)
    r.indoor = True
    r.set_description('small sunlit room', 'This circular room is lit by a shaft of sunlight in the center. The walls here are made of clay, baked like bricks by a fire.')
    r.add_names('room')
    r.add_adjectives('sunlit', 'circular', 'round')
    r.add_exit('north', 'domains.school.elementQuest.tapestries')
    r.add_exit('southwest', 'domains.school.elementQuest.potion_room')

    shaft = scenery.Scenery('shaft', 'shaft of sunlight', 'This shaft of sunlight glows down in the center of the room. Something about this shaft makes it very clear where the sun is shining and where it is not.')
    shaft.add_response(['step'], 'You step into the shaft of sunlight. It is warm.')
    r.insert(shaft)
    return r
