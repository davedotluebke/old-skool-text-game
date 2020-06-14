import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    bedroom = room.Room('cozy_room', roomPath)
    bedroom.indoor = True
    bedroom.set_description('cozy living space', ' This is a very cozy living space, with a coach, a fireplace, a velvet carpet, and a staircase in the corner. There is one door off of this room.')
    bedroom.add_exit('up', 'home.tate.bedroom')
    bedroom.add_exit('south', 'home.tate.entryway')
    coach = scenery.Scenery('coach','cozy nice coach', 'This cozy coach is very nice looking.')
    bed.add_adjectives('cozy', 'small')
    bed.add_response(['sit down'], 'you sit down, it is very comfy.', True, True)
    bed.add_response(['get up'], 'you get up.', emit_message='%s looks around the room.')
    bedroom.insert(coach)


    return bedroom