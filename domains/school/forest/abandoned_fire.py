import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('lonelyfire', roomPath)
    r.set_description('abandoned fire', 'You find yourself in a small chamber. On the the floor are several pieces of burnt wood arranged in a rough circle, as well as \
    a series of charcoal paintings on the walls. One of the pieces of wood looks sturdy enough to take. The cave continues to the northwest.')
    r.add_adjectives('dark')
    r.add_exit('northwest', 'domains.school.forest.oil_pool')
    r.add_exit('south', 'domains.school.forest.forest_cave_entry')

    burnt_log = scenery.Scenery('log','burnt log','This log is large enough to have come from a tree, and it\'s sharp edges suggest that it was cut.')
    burnt_log.add_response(['take', 'get'], 'The log begins to crumble in your hands when you try to take it.')
    burnt_log.add_adjectives('burnt','old','large','cut')
    burnt_log.move_to(r,True)

    log = gametools.clone('domains.school.forest.log')
    log.move_to(r,True)
    return r
