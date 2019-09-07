import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('waterfall_room', roomPath, indoor=True)
    r.set_description('underground waterfall', 'You find yourself on a ledge in a large and open room. '
    'To the west a cliff quickly drops off into a gushing stream. To the north a waterfall cascades over '
    'a cliff on the other side of the stream. A dark passage leads off to the southeast and another leads '
    'to the north.')
    r.add_exit('north', 'domains.centrata.firefile_area.cave.small_tunnel')
    r.add_exit('southeast', 'domains.school.forest.oil_pool')

    sign = scenery.Scenery('sign', 'wooden sign', 'This wooden sign has been attached - seemingly by magic - to the rock face. It appears to say something.')
    sign.add_response(['read'], 'The sign reads:\nSchool boundry. School property is to the south but not north. Continue at thy own risk.')
    sign.add_adjectives('wooden')
    sign.move_to(r, True)

    waterfall = scenery.Scenery('waterfall', 'gushing waterfall', 'This gushing waterfall plumets from a a higher part of the cave down into the stream.')
    waterfall.add_adjectives('gushing')
    waterfall.move_to(r,True)

    return r