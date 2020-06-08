import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    forest_road = room.Room('forest', roomPath)
    forest_road.set_description('forest road', 'You find yourself on a road through the forest. Trees grow thickly on either side. The road continues to the northwest and the southeast.')
    forest_road.add_exit('southeast', 'domains.school.forest.garden')
    forest_road.add_exit('northwest', 'domains.centrata.fields.school_gates')
    return forest_road
