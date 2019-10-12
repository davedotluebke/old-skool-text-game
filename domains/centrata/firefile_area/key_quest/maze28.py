import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage, you notice a huge slab of flowstone to the west.')
    r.add_exit('southeast', 'domains.centrata.firefile_area.key_quest.maze_entrance')
    r.add_exit('northwest', 'domains.centrata.firefile_area.key_quest.maze16')
    r.add_exit('west', 'domains.centrata.firefile_area.key_quest.maze49')

    flowstone = scenery.Scenery('flowstone', 'huge slab of flowstone', 'This slab of flowstone is huge and looks as if it is a waterfall frozen in motion.')
    flowstone.add_adjectives('huge', 'wet')
    flowstone.add_response(['climb', 'traverse'], "You try to climb the slab but can't find any good holds on it.")
    flowstone.unlisted = True
    flowstone.move_to(r, True)

    return r