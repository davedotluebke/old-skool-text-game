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
    return balcony
