import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    great_cavern = room.Room('cavern', roomPath)
    great_cavern.indoor = True
    great_cavern.set_description('great cavern', 'This is a massive cavern, with a seat carved into the rocks on the west end. You can hardly see the roof, but it is letting a tiny bit of light in.')
    great_cavern.add_exit('east', 'domains.school.dungeon.dungeon_hall')
    great_cavern.add_exit('southwest', 'domains.school.dungeon.small_tunnel')

    goblin = gametools.clone('domains.school.dungeon.goblin')
    great_cavern.insert(goblin)
    return great_cavern
