import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    bedroom = room.Room('cozy_bedroom', roomPath)
    bedroom.indoor = True
    bedroom.set_description('cozy bedroom', ' This is a very cozy bedroom, seememly belonging to a cottage. There is one door off of this room.')
    bedroom.add_exit('down', 'home.tate.tatelivingspace')
    bed = scenery.Scenery('bed','cozy bed', 'This bed looks cozy.')
    bed.add_adjectives('cozy', 'nice')
    bed.add_response(['lie'], 'you lie down and fall asleep.', True, True)
    bed.add_response(['get'], 'you get up.', emit_message='%s looks around the room.')
    bedroom.insert(bed)


    return bedroom