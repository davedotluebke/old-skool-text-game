import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    kitchen = room.Room('kitchen', roomPath, safe=True, indoor=True)
    kitchen.set_description('warm kitchen', 'This kitchen is mainly filled with a large pot over a central firepit. On one side you see a clay oven. A few metal cabinets hang high on one wall.')
    kitchen.add_adjectives('warm', 'cozy')
    kitchen.add_exit('west', 'domains.school.school.fire_lounge')

    central_pot = gametools.clone('domains.school.school.central_pot')
    central_pot.move_to(kitchen)

    clay_oven = gametools.clone('domains.school.school.clay_oven')
    clay_oven.move_to(kitchen)

    metal_cabinets = gametools.clone('domains.school.school.metal_cabinets')
    metal_cabinets.move_to(kitchen)
    return kitchen
