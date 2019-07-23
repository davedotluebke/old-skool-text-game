import room
import gametools
import domains.character_creation.mirror as mirror

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('gender_room', roomPath)
    r.set_description('boundless room', 'You find yourself in a room with a glass floor and walls. '
        'You see three mirrors, one north, one south, and one east.')

    female = mirror.Mirror('a female &s&u, smiling back at you', 'domains.character_creation.adjective1', gender="female")
    female.add_adjectives('north')
    r.insert(female)

    male = mirror.Mirror('a male &s&u, smiling back at you', 'domains.character_creation.adjective1', gender="male")
    male.add_adjectives('south')
    r.insert(male)

    other = mirror.Mirror('a nondescript &s&u, smiling back at you', 'domains.character_creation.adjective1')
    other.add_adjectives('east')
    r.insert(other)

    return r
