import room
import gametools
import domains.character_creation.mirror as mirror

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('empty_room', roomPath)
    r.set_description('empty void', 'You find yourself in an empty void with a translucent floor. '
        'You see four mirrors, one north, one south, one east, and one west.')

    human = mirror.Mirror('a human, smiling back at you', 'domains.character_creation.gender', species='human')
    human.add_adjectives('north', 'human')
    r.insert(human)

    elf = mirror.Mirror('an elf, smiling back at you', 'domains.character_creation.gender', species='elf')
    elf.add_adjectives('south', 'elf')
    r.insert(elf)

    dwarf = mirror.Mirror('a dwarf, smiling back at you', 'domains.character_creation.gender', species='dwarf')
    dwarf.add_adjectives('east', 'dwarf')
    r.insert(dwarf)

    gnome = mirror.Mirror('a gnome, smiling back at you', 'domains.character_creation.gender', species='gnome')
    gnome.add_adjectives('west', 'gnome')
    r.insert(gnome)
    return r
    