import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    balcony = room.Room('balcony', roomPath)
    balcony.set_description('small balcony', 'This small balcony overlooks the school grounds. To your west you see a waterfall, '
    'and to your south you see a large forest. ')
    balcony.add_adjectives('small')
    balcony.add_exit('north', 'domains.school.school.arena')

    waterfall = scenery.Scenery('waterfall', 'waterfall', 'This beautiful waterfall stands to the west of the balcony.', unlisted=True)
    waterfall.move_to(balcony, True)

    forest = scenery.Scenery('forest', 'large forest', 'This large forest continues the entire forseeable distance to the south.', unlisted=True)
    forest.move_to(balcony, True)
    return balcony
