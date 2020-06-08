import room
import gametools
import thing
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('hall', roomPath)
    r.indoor = True
    r.set_description('large hall', 'You find yourself in a large stone hall with a stone staircase leading up to an archway. The archway has been painted red, orange, and yellow.')
    r.add_adjectives('large')
    r.add_exit('east', 'domains.school.elementQuest.warm_passage')
    r.add_exit('northwest', 'domains.school.elementQuest.lava_view')

    stairs = scenery.Scenery('staircase', 'stone staircase', 'This large stone staircase rises to an archway to the next room.', unlisted=True)
    stairs.add_names('stairs', 'stair')
    stairs.add_response(['climb'], 'You climb the staircase.')
    stairs.add_response(['descend'], 'You walk down the staircase.', intrans=True)
    r.insert(stairs)

    archway = scenery.Scenery('archway', 'painted archway', 'This archway has been painted red, orange, and yellow.', unlisted=True)
    archway.add_names('arch')
    archway.add_adjectives('painted', 'red', 'orange', 'yellow')
    r.insert(archway)
    return r
