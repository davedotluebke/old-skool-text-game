import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    crawlway = room.Room('crawlway', roomPath)
    crawlway.indoor = True
    crawlway.set_description('tight crawlway', 'This crawlway is a tight squeeze, but you fit through. The monster would not, however.')
    crawlway.add_exit('north', 'domains.school.dungeon.dungeon_hall')
    crawlway.add_exit('southeast', 'domains.school.cave.lair')
    crawlway.add_adjectives('tight')
    crawlway.set_max_volume_carried(70)
    return crawlway
