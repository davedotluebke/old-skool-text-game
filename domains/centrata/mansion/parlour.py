import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('parlour', roomPath, indoor=True)
    r.set_description('well-furnished parlour', 'You step into a well-furnished parlour, complete with several sofas and armchairs. The wallpaper is a dark red, pairing with the green of the furniture. Passages lead south and northwest, while there are doors to the north and the southwest.')
    r.add_exit('south', 'domains.centrata.mansion.office')

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
