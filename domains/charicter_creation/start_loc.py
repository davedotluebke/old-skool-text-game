import room
import gametools
import mirror

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('empty_room', roomPath)
    r.set_description('empty void', 'You find yourself in an empty void with a translucent floor. You see four mirrors, one north, one south, one east, and one west.')

    human = mirror.Mirror('a human, smiling back at you', 'domains.charicter_creation.gender')
    human.add_race = 'human'
    human.add_adjectives('north')
    r.insert(human)

    elf = mirror.Mirror('an elf, smiling back at you', 'domains.charicter_creation.gender')
    elf.add_race = 'elf'
    elf.add_adjectives('south')
    r.insert(elf)

    dwarf = mirror.Mirror('a dwarf, smiling back at you', 'domains.charicter_creation.gender')
    dwarf.add_race = 'dwarf'
    dwarf.add_adjectives('east')
    r.insert(dwarf)

    gnome = mirror.Mirror('a gnome, smiling back at you', 'domains.charicter_creation.gender')
    gnome.add_race = 'gnome'
    gnome.add_adjectives('west')
    r.insert(gnome)
    return r
    