import creature

def clone():
    rat = creature.NPC('rat', __file__, 2)
    rat.set_description('nasty rat', 'This is a nasty rat with gleaming red eyes.')
    rat.set_weight(1000)
    rat.set_volume(1)
    rat.set_combat_vars(5, 10, 10, 60)
    rat.set_default_weapon("sharp teeth", 5, 10, 1)
    rat.forbid_room('domains.school.forest.forest1')
    rat.forbid_room('domains.school.cave.cave')
    return rat