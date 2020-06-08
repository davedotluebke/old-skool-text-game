import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    dim_forest = room.Room('forest', roomPath)
    dim_forest.set_description('dim forest', 'You enter a dim forest, with trees blocking most of the light. You can barely make out the gaps between the trees.')
    dim_forest.add_exit('east', 'domains.school.forest.pine_forest')
    dim_forest.add_exit('northwest', 'domains.school.forest.gloomy_forest')
    return dim_forest
