import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    kitchen = room.Room('kitchen', roomPath)
    kitchen.indoor = True
    kitchen.set_description('dusty kitchen with 50-year-old appliances and decorations', 'This kitchen looks about 50 years old and is very dusty, but it appears to still be usable.')
    kitchen.add_exit('northeast', 'domains.school.forest.entryway')
    kitchen.add_exit('southeast', 'domains.school.forest.hallway')

    cabinets = gametools.clone('domains.school.forest.cabinets')
    kitchen.insert(cabinets)

    table = gametools.clone('domains.school.forest.table')
    kitchen.insert(table)

    sink = gametools.clone('domains.school.forest.sink')
    kitchen.insert(sink)
    return kitchen