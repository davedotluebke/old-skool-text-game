import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    maze_entrance = room.Room('small cavern', roomPath, indoor=True)
    maze_entrance.set_description('small cavern','This is a small cavern. To the the east and west two winding passageways lead off into the darkness.')
    maze_entrance.add_exit('east', 'domains.centrata.key_quest.maze28')
    maze_entrance.add_exit('west', 'domains.centrata.key_quest.maze41')

    ruby = gametools.clone('home.johanna.house.ruby')
    maze_entrance.insert(ruby)

    emerald = gametools.clone('home.johanna.house.emerald')
    maze_entrance.insert(emerald)
    return maze_entrance
