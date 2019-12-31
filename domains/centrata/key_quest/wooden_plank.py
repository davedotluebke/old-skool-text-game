import gametools
import room
import scenery

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('plank', roomPath)
    r.set_description('precarious plank', 'You find yourself balanced precariously on a plank above the shack. It is surrounded by caution tape.')
    r.add_adjectives('precarious')
    r.add_exit('down', 'domains.school.forest.shack')
    r.add_exit('west', 'domains.centrata.key_quest.treetop2', caution_tape_msg='The bridge to the west is surrounded by caution tape, and you decide not to test its strength.')
    return r
