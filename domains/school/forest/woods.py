import gametools
import room
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    woods = room.Room('woods', pref_id=roomPath)
    woods.set_description('bright and cheerful woods', 'Theese woods have happy birdsongs and pretty trees. They are bright.')
    woods.add_exit('west', 'domains.school.forest.entryway')
    woods.add_exit('north', 'domains.school.forest.forest1')
    woods.add_exit('south', 'domains.school.forest.clearing')

    bag = gametools.clone('domains.school.forest.bag')
    woods.insert(bag)

    flashlight = gametools.clone('domains.school.forest.flashlight')
    woods.insert(flashlight)

    beech = scenery.Scenery("beech", "old beech tree full of carvings", 
    "This large old beech tree has been scarred with the reminders of many passers-by, who decided to immortalize their visit by carving their initials into the tree.")
    beech.add_names("tree")
    beech.add_adjectives("old", "beech", "carved")
    beech.add_response(["carve"], "You think about carving your own initials into the tree, but an uneasy feeling--as if the forest itself is watching--makes you stop.")
    woods.insert(beech)

    bird = gametools.clone('domains.school.forest.bird')
    woods.insert(bird)

    return woods
