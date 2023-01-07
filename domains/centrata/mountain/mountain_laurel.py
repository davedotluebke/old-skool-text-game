import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    trail = room.Room('trail', roomPath)
    trail.set_description('winding trail through the mountains', 'You find yourself on a winding trail through the dense mountain laurel. To the east the trail leads steeply down the mountain. To the west the trail leads up towards the peak.')
    trail.add_exit('east', 'domains.centrata.mountain.woods')
    trail.add_exit('west', 'domains.centrata.mountain.clifftop')

    mountain_laurel = scenery.Scenery("laurel", "thick mountain laurel", "This mountain laurel is thick and dense. It is in full bloom, with brilliant pink and white flowers sprouting up from between the green leaves.", unlisted=True)
    mountain_laurel.add_adjectives("mountain")
    mountain_laurel.add_names('bud', 'buds')
    mountain_laurel.add_response(['pick'], 'You attempt to pick the mountain laurel, but the flowers are too firmly attached to the stems.')
    trail.insert(mountain_laurel, True)
    
    return trail
