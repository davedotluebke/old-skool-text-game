import gametools
import room
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    pine_forest = room.Room('pine forest', pref_id=roomPath)
    pine_forest.set_description('pine forest', 'You enter a thick forest of tall pines. You can barely see the sky above you.')
    pine_forest.add_exit('east', 'domains.school.forest.garden')
    pine_forest.add_exit('west', 'domains.school.forest.dim_forest')

    pine = scenery.Scenery('pine', 'sturdy pine', 'This sturdy pine shoots up out of the ground and makes its way to the sky.')
    pine.unlisted = True
    pine.add_response(['climb'], 'Unfortunately, this pine has very few lower branches that you can get a hold of.')
    pine.move_to(pine_forest, force_move=True)
    
    return pine_forest