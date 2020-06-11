import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('balcony', roomPath)
    r.set_description('balcony', 'This is a large balcony overlooking some tall, steep mountains. You notice a large number of birdfeeders here.')
    r.add_adjectives('bedroom', 'birdfeeder', 'mountain', 'tower')
    
    east_door = doors_and_windows.Door('door', 'glass door', 'This tinted glass door leads back into the tower.', 'domains.school.elementQuest.bedroom', 'east')
    east_door.add_adjectives('glass', 'bedroom')
    r.insert(east_door)

    feeder_one = scenery.Scenery('feeder', 'cylendrical bird feeder', 'This is a small cylendrical bird feeder with several perches.')
    feeder_one.add_adjectives('bird', 'cylendrical', 'small')
    feeder_one.add_response(['take', 'get', 'steal', 'remove', 'destroy', 'break'], 'You consider removing the birdfeeders, but decide the birds would not like it.')
    r.insert(feeder_one)

    feeder_two = scenery.Scenery('feeder', 'hopper style bird feeder', 'This is an enormous hopper style bird feeder.')
    feeder_two.add_adjectives('bird', 'hopper', 'style', 'hopper-style', 'enormous')
    feeder_two.add_response(['take', 'get', 'steal', 'remove', 'destroy', 'break'], 'You consider removing the birdfeeders, but decide the birds would not like it.')
    r.insert(feeder_two)

    feeder_three = scenery.Scenery('feeder', 'suet feeder', 'This is a small suet feeder.')
    feeder_three.add_adjectives('bird', 'suet', 'small')
    feeder_three.add_response(['take', 'get', 'steal', 'remove', 'destroy', 'break'], 'You consider removing the birdfeeders, but decide the birds would not like it.')
    r.insert(feeder_three)

    mountains = scenery.Scenery('mountains', 'mountains', 'These mountains are tall, steep, and covered in snow in some sections.', unlisted=True)
    mountains.add_adjectives('tall', 'steep', 'snowy')
    r.insert(mountains)
    
    return r