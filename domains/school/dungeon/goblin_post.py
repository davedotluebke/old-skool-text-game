import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    goblin_post = room.Room('square room', roomPath)
    goblin_post.indoor = True
    goblin_post.set_description('square, torchlit room', 'You are in a square room lit by torches. Above the tunnel to the east there is writing that says, "All who dare to come in will perish."')
    goblin_post.add_exit('east', 'domains.school.dungeon.dark_tunnel')
    goblin_post.add_names('room', 'hall', 'post')
    goblin_post.add_adjectives('spooky', 'torchlit', 'square')

    goblin = gametools.clone('domains.school.dungeon.goblin')
    goblin_post.insert(goblin)

    master_goblin = gametools.clone('domains.school.dungeon.master_goblin')
    goblin_post.insert(master_goblin)
    return goblin_post
