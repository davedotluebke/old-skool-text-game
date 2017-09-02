import creature
import gametools
import thing

def take_stuff(horster):
    if not horster.location:
        return
    for i in horster.location.contents:
        if not isinstance(i, creature.Creature):
            if not i.fixed:
                i.move_to(horster)
                return

def clone():
    scavenger = creature.NPC('horster', __file__, 1)
    scavenger.set_description('large red horster', 'This is a bright red horster. It scans the ground, carefully, looking for things. It has a huge pile of things in an old bag it has.')
    scavenger.add_adjectives('large', 'red')
    scavenger.choices.append(take_stuff)
    scavenger.act_frequency = 2

    bag = gametools.clone('domains.school.forest.bag')
    scavenger.insert(bag)
    return scavenger