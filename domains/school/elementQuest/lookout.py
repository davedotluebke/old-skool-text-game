import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('lookout', roomPath)
    r.set_description('lookout', 'This round lookout overlooks the tall, steep mountains surrounding the area. There is a staircase leading down.')
    r.add_exit('down', 'domains.school.elementQuest.living_space')

    mountains = scenery.Scenery('mountains', 'mountains', 'These mountains are tall, steep, and covered in snow in some sections.', unlisted=True)
    mountains.add_adjectives('tall', 'steep', 'snowy')
    r.insert(mountains)

    return r
