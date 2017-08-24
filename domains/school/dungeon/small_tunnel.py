import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    small_tunnel = room.Room('tunnel', roomPath)
    small_tunnel.set_description('small tunnel', 'You are in a small tunnel, which turns into a crawlway to the south. There is an exit off the tunnel to the west whcih has a yellow glow comming from the end. A dark tunnel leads north.')
    small_tunnel.add_exit('northeast', 'domains.school.dungeon.great_cavern')
    small_tunnel.add_exit('west', 'domains.school.dungeon.trap')
    small_tunnel.add_exit('south', 'domains.school.dungeon.entrance')
    small_tunnel.add_adjectives('small')
    return small_tunnel
