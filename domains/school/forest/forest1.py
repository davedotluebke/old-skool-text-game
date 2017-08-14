import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    forest_one = room.Room('forest', roomPath)
    forest_one.set_description('nice forest', 'This is an ancient forest with towering trees. They must be hundreds of years old at least.')
    forest_one.add_exit('south', 'domains.school.forest.woods')
    forest_one.add_exit('east', 'domains.school.forest.forest2')
    forest_one.add_exit('northwest', 'domains.school.forest.forest3')
    forest_one.add_adjectives('ancient','towering','nice')

    elm = scenery.Scenery("elm", "massive old elm tree", "This huge elm tree must be over a hundred years old. You are tempted to hug it.")
    elm.add_names("tree")
    elm.add_adjectives("big", "massive", "old", "elm")
    elm.add_response(["hug", "hold"], "You give the old elm tree a long hug, and feel deeply satisfied.", emit_message='%s hugs the old elm tree, and you want to too.')
    elm.add_response(["climb"], "The trunk is too broad to wrap your arms around, and the lowest branches are far too high to reach.")
    forest_one.insert(elm)
    pine_one = scenery.Scenery('pine', 'old sturdy pine tree','This pine tree has clearly been here for quite a while. It seems strong and has some low branches you think you can reach.')
    pine_one.add_names('pine','tree')
    pine_one.add_adjectives('old','sturdy','pine')
    pine_one.add_response(['climb'], "Unfortunately, the lower branches are not as strong as the sturdy trunk, and you can't seem to get a hold of the higher ones.", emit_message='%s reaches for the lower branches, but they break off.')
    forest_one.insert(pine_one)

    return forest_one