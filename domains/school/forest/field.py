import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    field = room.Room('field', roomPath)
    field.set_description('field with a small shack on the west side', 'This field is on the outskirts of Firlefile sorcery school and has a small shack on the west side.')
    field.add_exit('west', 'domains.school.forest.forest2')
    field.add_exit('in', 'domains.school.forest.shack')
    field.add_exit("north",'domains.school.forest.garden')
    field.add_exit('northeast', 'domains.school.school.grand_entry')
    field.add_exit('southeast', 'domains.school.forest.waterfall')

    butterfly = gametools.clone('domains.school.forest.butterfly')
    field.insert(butterfly)

    return field