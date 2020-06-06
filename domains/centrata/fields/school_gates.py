import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    school_gates = room.Room('school_gates', roomPath, safe=True)   # TODO: Actual gate functionality: players must "open gate" to pass through, etc.
    school_gates.set_description('school gates', 'You find yourself at the magnificent gates of Firefile Scorcery School. '
    'On the north side of the gate, a road leads to the northwest into a prairie. On the south side, a road leads southeast '
    'into a thick forest.')
    school_gates.add_exit('northwest', 'domains.centrata.fields.road_one')
    school_gates.add_exit('southeast', 'domains.school.forest.forest_road')
    return school_gates
