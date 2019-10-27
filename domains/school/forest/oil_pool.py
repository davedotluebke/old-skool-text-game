import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('oil_pool', roomPath, 0, indoor=True)
    r.set_description('damp and dark room', 'You find yourself in a damp and dark room. In one corner a small pool of oil covers the ground. You hear the sound of rushing water coming from the northwest.')
    r.add_exit('southeast', 'domains.school.forest.abandoned_fire')
    r.add_exit('northwest', 'domains.school.forest.underground_waterfall')

    oil_pool = scenery.Scenery('pool', 'oil pool', 'This pool of oil lies in the southwest corner of the room. It looks very slick but thin.')
    oil_pool.add_adjectives('oil', 'slick', 'thin')
    oil_pool.add_response(['take', 'get'], 'The oil is far to thinly spread to take.')
    oil_pool.add_response(['drink'], 'You think about drinking the oil, but very quickly change your mind.')
    oil_pool.move_to(r,True)

    return r
