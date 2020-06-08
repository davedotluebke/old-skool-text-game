import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    bedroom = room.Room('bedroom', roomPath)
    bedroom.indoor = True
    bedroom.set_description('dusty bedroom', 'The bare board walls of this bedroom are dusty. A musty smell fills the air.')
    bedroom.add_exit('northwest', 'domains.school.forest.hallway')
    bed = scenery.Scenery('bed','decrepit old bed', 'This decrepit bed supports a bare stained mattress and is covered with a thick layer of dust.')
    bed.add_adjectives('old', 'decrepit')
    bed.add_response(['sleep'], 'You briefly consider sleeping on the dusty, soiled mattress but quickly think better of it.', True, True)
    bed.add_response(['make'], 'You look around for sheets or blankets but see nothing suitable with which to make the bed.', emit_message='%s looks around the room.')
    bedroom.insert(bed)

    sword = gametools.clone('domains.school.forest.sword')
    bedroom.insert(sword)
    leather_suit = gametools.clone('domains.school.forest.leather_suit')
    bedroom.insert(leather_suit)

    return bedroom
