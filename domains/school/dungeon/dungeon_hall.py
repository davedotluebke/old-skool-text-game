import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    dungeon_hall = room.Room('dungeon hall', pref_id=roomPath)
    dungeon_hall.indoor = True
    dungeon_hall.set_description('dungeon hall', 'This is a old cave which has moss growing on the damp walls. It seems like it was made for a purpouse. There are tunnels to the north, south, and west, and a crawlway to the east.')
    dungeon_hall.add_exit('east', 'domains.school.dungeon.crawlway')
    dungeon_hall.add_exit('west', 'domains.school.dungeon.great_cavern')
    dungeon_hall.add_exit('south', 'domains.school.dungeon.dead_end')
    dungeon_hall.add_exit('north', 'domains.school.dungeon.dark_tunnel')
    dungeon_hall.add_names('cave', 'dungeon', 'hall')
    dungeon_hall.add_adjectives('purposefull')
    return dungeon_hall
