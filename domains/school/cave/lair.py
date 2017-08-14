import domains.school.caveComplex as cave_mod
import room
import gametools
import thing

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    lair = cave_mod.Lair('lair', roomPath)
    lair.set_description('monster\'s lair', 'This is a lair where the terrible monster hides. It has a wall with clubs hanging on it. There is a crawlway to the northwest.')
    lair.add_adjectives("monster's")
    lair.add_exit('east', 'domains.school.cave.cave')
    lair.monster = gametools.clone('domains.school.cave.monster')
    lair.insert(lair.monster)

    return lair
