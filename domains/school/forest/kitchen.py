import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    kitchen = room.Room('kitchen')
    kitchen.set_description('dusty kitchen with 50-year old apliences and decorations', 'This kitchen looks about 50 years old, and is very dusty but apears still useable.')
    kitchen.add_exit('northeast', 'domains.school.forest.entryway')
    kitchen.add_exit('southeast', 'domains.school.forest.hallway')

    cabinets = gametools.clone('domains.school.forest.cabinets')
    kitchen.insert(cabinets)

    table = gametools.clone('domains.school.forest.table')
    kitchen.insert(table)
    return kitchen