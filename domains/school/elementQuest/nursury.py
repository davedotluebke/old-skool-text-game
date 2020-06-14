import room
import gametools
import thing
import scenery
import doors_and_windows


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('nursury', roomPath)
    r.indoor = True
    r.set_description('multi-porpuse nursery', 'You enter a small carpeted room. On the north side you see a changing table with a painting hanging over it, a cradle, and some cabinets. On the south side of the room you see five flower pots.')
    r.add_adjectives('windy')
    r.add_exit('west', 'domains.school.elementQuest.living_space')

    sunset_portriat = scenery.Scenery ('portriat', 'portriat', 'This portriat show a coopers hawk flying off into the sunset over some mountains. You are awed by the beauty of it.', unlisted=True)
    sunset_portriat.add_names('portriat', 'painting')
    sunset_portriat.add_adjectives('sunset', 'hawk', 'coopers', 'beautiful', 'awe inspiring')
    sunset_portriat.add_response(['take','steal','touch'], 'As you start to reach out you remember the plaque in th portriat gallery which reminds you not to touch any of the paintings.')
    r.insert(sunset_portriat)

    crib = scenery.Scenery ('crib', 'wooden crib', 'This is a empty wooden crib is very normal crib, it has metal bars on the sides and is empty.', unlisted=True)
    crib.add_adjectives('infint', 'bed', 'baby', 'empty')
    crib.add_names('bed', 'cradle')
    crib.add_response(['take', 'steel', 'remove', 'move'], 'Try as you might, you can not seem to be able to move the crib. It feels as if magic is holding it in place.')
    r.insert(crib)

    cabinets = gametools.clone('domains.school.elementQuest.nursury_cabinets')
    r.insert(cabinets)

    flower_pot = gametools.clone('domains.school.elementQuest.flower_pot')
    flower_pot.plurality = 3
    r.insert(flower_pot)

    ground_cover_pot = gametools.clone('domains.school.elementQuest.ground_cover_pot')
    ground_cover_pot.plurality = 2
    r.insert(ground_cover_pot)

    changing_table = gametools.clone('domains.school.elementQuest.changing_table')
    r.insert(changing_table)

    price_tag_bundle = gametools.clone('domains.school.elementQuest.price_tag_bundle')
    r.insert(price_tag_bundle)

    return r
