import room
import gametools
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('balcony', roomPath, indoor = False)
    r.set_description('sunny balcony', 'You walk out onto a sunny stone balcony. The edge of the balcony is lined with a stone wall. From the blacony you can see jagged mountains that go on as far as the eye can see.')
    r.add_exit('west', 'domains.school.elementQuest.sauna_room')
    r.add_adjectives('sunny', 'stone', 'walled')

    wall = scenery.Scenery('wall', 'stone wall', 'This is a stuby sturdy stone wall that surrounds the balcony.', unlisted=True)
    wall.add_adjectives('sturdy', 'stone')
    wall.add_response(['break', 'destroy', 'pound', 'crush'], 'You think about it but then you think that you probably shouldn\'t becuase it would be dangerous.')
    r.insert(wall)

    towel = gametools.clone('domains.school.elementQuest.towel')
    r.insert(towel)

    return r
