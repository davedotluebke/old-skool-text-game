# NPC factory: This module creates a random creature based on a coordinate pair, rather than a specific one
import random
import creature

def clone(coords=(0,0,0)):
    monster_types = {'orc': 10, 'goblin': 40, 'hobgoblin': 20, 'kobold': 30}
    type_range_values = []
    for p in list(monster_types):
        for q in range(0, monster_types[p]):
            type_range_values.append(p)

    monster_type = type_range_values[random.randint(0,99)]
    monster = creature.NPC('%s' % monster_type, __file__, random.randint(1,2))
    monster.set_description('%s' % monster_type, 'This is a %s.' % monster_type)
    monster.set_combat_vars(random.randint(8, 16), random.randint(5, 30), random.randint(15,25), random.randint(5, 30))
    # TODO: Base these attributes on monster type and coordinates
    return monster
