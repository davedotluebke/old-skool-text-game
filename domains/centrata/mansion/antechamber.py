import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('antechamber', roomPath, indoor=True)
    r.set_description('spacious antechamber', 'You stand inside a spacious antechamber. A rose-tinted chandelier hangs over you. The walls are panelled with mahogany. There are doors to the north and the south.')
    
    antechamber_door = keyed_door.KeyedDoor('door', 'mahogany door', 'This mahogany door has bevelled edges around two indented panels.', 'domains.centrata.mansion.parlour', 'south', 'domains.centrata.mansion.interior_door_key')
    antechamber_door.add_adjectives('mahogany', 'wooden', 'bevelled')
    antechamber_door.unlocked = True
    r.insert(antechamber_door, True)
    
    front_door = keyed_door.KeyedDoor('door', 'front door', 'This grandiose front door is made of mahogany. It has elaborate carvings of dragons on it.', 'domains.centrata.mansion.porch', 'north', 'domains.centrata.mansion.house_key')
    front_door.add_adjectives('large', 'grandiose', 'front')
    front_door.locked = True

    large_sofa = scenery.Scenery('sofa', 'large green sofa', 'This large dark green sofa is covered in a soft felt material.', unlisted=True)
    large_sofa.add_adjectives('large', 'green', 'soft', 'felt')
    large_sofa.add_response(['sit', 'lie', 'relax'], 'You relax on the sofa. The felt covering feels soft.')
    large_sofa.add_response(['move', 'take', 'get'], 'The large sofa is far too heavy to move.')
    r.insert(large_sofa, True)
    
    small_sofa = scenery.Scenery('sofa', 'small green sofa', 'This small dark green sofa is covered in a soft felt material.', unlisted=True)
    small_sofa.add_adjectives('small', 'dark', 'green', 'soft', 'felt')
    small_sofa.add_response(['sit', 'lie', 'relax'], 'You relax on the sofa. The felt covering feels soft.')
    small_sofa.add_response(['move', 'take', 'get'], 'Despite being the smaller of the sofas, the small green sofa is still far too heavy to move.')
    r.insert(small_sofa, True)
    
    armchair = scenery.Scenery('armchair', 'large green armchair', 'This large dark green armchair is covered in a soft felt material.', unlisted=True)
    armchair.add_adjectives('large', 'green', 'soft', 'felt')
    armchair.add_response(['sit', 'lie', 'relax'], 'You relax in the armchair. The felt covering feels soft.')
    armchair.add_response(['move', 'take', 'get'], 'Despite being smaller than the two sofas, the armchair is far too heavy to move.')
    r.insert(armchair, True)
    
    wallpaper = scenery.Scenery('wallpaper', 'red pattered wallpaper', 'This red pattered wallpaper is a dark red, with a slightly brighter red patterning showing long serpents.', unlisted=True)
    wallpaper.add_adjectives('red', 'pattered', 'serpent')
    r.insert(wallpaper, True)

    return r
