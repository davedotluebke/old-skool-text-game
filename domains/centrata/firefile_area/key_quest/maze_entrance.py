import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    maze_entrance = room.Room('small cavern', roomPath)
    maze_entrance.set_description('This is a small cavern. To the the east and west two winding passageways lead off into the darkness.')
    maze_entrance.add_exit('east', 'domains.centrata.firefile_area.key_quest.maze28')
    maze_entrance.add_exit('west', 'domains.centrata.firefile_area.key_quest.maze41')

    ruby = gametools.clone('home.scott.house.ruby')
    maze_entrance.insert(ruby)

    emerald = gametools.clone('home.scott.house.emerald')
    maze_entrance.insert(emerald)
    return maze_entrance
