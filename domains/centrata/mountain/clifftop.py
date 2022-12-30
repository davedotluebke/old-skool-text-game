import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    trail = room.Room('trail', roomPath)
    trail.set_description('trail on a high ridge', 'You find yourself on a trail on a high treeless ridge. To the north and the south cliffs lead down to the forest below. To the east the trail descends into a thicket of mountain laurel. To the west the trail ascends to a small hut.')
    trail.add_exit('east', 'domains.centrata.mountain.mountain_laurel')
    trail.add_exit('west', 'domains.centrata.mountain.peak')

    cliff = scenery.Scenery("cliff", "large cliff", "This granite cliff is covered in loose rocks. You can hardly make out the trees at the bottom.")
    cliff.add_response(['climb', 'descend', 'ascend'], 'The rocks are too lose for your to be able to climb.')
    trail.insert(cliff, True)
    
    return trail
