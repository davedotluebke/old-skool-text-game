import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    forest_two = room.Room('forest', roomPath)
    forest_two.set_description('nice forest', 'This is an ancient forest with towering trees. They must be hundreds of years old at least.')
    forest_two.add_exit('west', 'domains.school.forest.forest1')
    forest_two.add_exit('east', 'domains.school.forest.field')
    forest_two.add_adjectives('ancient','towering','nice')
    
    pine_two = scenery.Scenery('pine', 'old sturdy pine tree','This pine tree has clearly been here for quite a while. It seems strong and has some low branches you think you can reach.')
    pine_two.add_names('pine','tree')
    pine_two.add_adjectives('old','sturdy',)
    pine_two.add_response(['climb'], "Unfortunatley, the lower branches are not as strong as the sturdy trunk, and you can't seem to get a hold of the higher ones.", emit_message='%s reaches for the lower branches, but they break off.')
    forest_two.insert(pine_two)

    return forest_two