import creature

def clone():
    monster = creature.NPC('monster', 'domains.school.cave.monster', Thing.ID_dict['nulspace'].game, 2)
    monster.set_description('terrible monster', 'This is a horrible monster. You want to run away from it.')
    monster.set_combat_vars(50, 60, 80, 40)
    monster.act_frequency = 1
    monster.set_volume(100)
    monster.set_weight(500000)
    return monster
