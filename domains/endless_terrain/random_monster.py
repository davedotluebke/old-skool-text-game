# NPC factory: This module creates a random creature based on a coordinate pair, rather than a specific one
import random
import creature
from collections import namedtuple

Monster_stats = namedtuple('MonsterData', ['name', 'plural_name', 'probability', 'av_ac', 'av_combat', 'av_strength', 'av_dex'])

def clone(coords=(0,0,0)):
    # probabilities should add up to 100
    monster_types = [Monster_stats('orc','orcs',probability=10,av_ac=20,av_combat=40,av_strength=30,av_dex=40), 
                     Monster_stats('goblin','goblins',probability=40,av_ac=10,av_combat=30,av_strength=20,av_dex=40),
                     Monster_stats('hobgoblin','hobgoblins',probability=20,av_ac=30,av_combat=50,av_strength=40,av_dex=60),
                     Monster_stats('kobold','kobolds',probability=30,av_ac=10,av_combat=20,av_strength=10,av_dex=40)]
    rand = random.randrange(1,100)
    for m in monster_types:
        rand -= m.probability
        if rand <= 0: 
            break

    monster = creature.NPC(m.name, __file__, random.randint(1,2))
    monster.set_description(m.name, 'This is a %s.' % m.name)
    # TODO: vary these attributes by up to +/- 10% of the average
    monster.set_combat_vars(m.av_ac, m.av_combat, m.av_strength, m.av_dex)
    return monster
