import creature
import thing

def clone():
    goblin = creature.NPC('goblin', __file__, thing.Thing.ID_dict['nulspace'].game, 1)
    goblin.set_description('green goblin', 'This green goblin is staring at you. It keeps staring at you, then looks around the room.')
    goblin.add_adjectives('horrid', 'creepy', 'mean', 'green')
    goblin.set_weight(200/2.2)
    goblin.set_volume(71)
    goblin.armor_class = 100
    goblin.combat_skill = 70
    goblin.strength = 35
    goblin.dexterity = 50
    goblin.add_script('If anyone dares to enter our cave...')
    goblin.add_script('Whoever attacked us will be punished...')
    return goblin
