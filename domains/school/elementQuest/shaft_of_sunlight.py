import room
import gametools
import thing
import scenery
import container

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('sunlit room', roomPath)
    r.indoor = True
    r.set_description('small sunlit room', 'This circular room is lit by a shaft of sunlight in the centre. The walls here are made of clay, baked like bricks by a fire.')
    r.add_names('room')
    r.add_adjectives('sunlit', 'circular', 'round')
    r.add_exit('north', 'domains.school.elementQuest.tapestries')
    r.add_exit('southwest', 'domains.school.elementQuest.warm_passage')

    shaft = scenery.Scenery('shaft', 'shaft of sunlight', 'This shaft of sunlight glows down in the centre of the room. Something about this shaft makes it very clear where the sun is shining and where it is not.')
    shaft.add_names('sunlight')
    shaft.add_response(['step'], 'You step into the shaft of sunlight. It is warm.')
    r.insert(shaft)

    match = gametools.clone('domains.school.elementQuest.match')
    r.insert(match)
    
    return r
