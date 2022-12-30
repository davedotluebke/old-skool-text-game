import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    mountain_base = room.Room('base', roomPath)
    mountain_base.set_description('base of a mountain', 'You stand at the base of a large mountain. To your west a trail continues winds its way up the mountain. The trail also leads to the east.')
    mountain_base.add_exit('east', 'domains.centrata.fields.road_five')
    mountain_base.add_exit('west', 'domains.centrata.mountain.woods')

    mountain = scenery.Scenery("mountain", "tall imposing mountain", "This tall imposing mountain, mostly forested, looms over this spot. It looks difficult to climb.", unlisted=True)
    mountain_base.insert(mountain, True)

    acleð = gametools.clone('domains.centrata.mountain.acleð')
    mountain_base.insert(acleð, True)

    return mountain_base
