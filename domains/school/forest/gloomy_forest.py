import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('gloomyforest', roomPath)
    r.set_description('gloomy forest', 'This is a very gloomy forest. Here the trail leading here from the south disinegrates to the point you can\'t see it anymore.')
    r.add_adjectives('gloomy')
    r.add_exit('south', 'domains.school.forest.dark_forest')

    witherd_boulder = scenery.Scenery('boulder', 'withered boulder', 'This withered boulder is covered in an ancient lichen.')
    witherd_boulder.add_response(['sit'], 'You consider sitting on the boulder, but the forest around is making you feel like you should stay on your toes.')
    witherd_boulder.add_response(['move'], 'The boulder is too heavy to move.')
    r.insert(witherd_boulder)

    return r