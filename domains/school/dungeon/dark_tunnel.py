import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    dark_tunnel = room.Room('tunnel', light=0, pref_id=roomPath)
    dark_tunnel.indoor = True
    dark_tunnel.set_description('crude walled tunnel', 'This tunnel has crude walls. Something about this tunnel seems eerie.')
    dark_tunnel.add_exit('south', 'domains.school.dungeon.dungeon_hall')
    dark_tunnel.add_exit('north', 'domains.school.dungeon.goblin_post')
    dark_tunnel.add_adjectives('dark', 'eerie')
    return dark_tunnel
