import creature
import gametools

def clone():
    giant = creature.NPC('giant', __file__, aggressive=2)
    giant.set_description('massive giant', 'This giant towers over you. It looks down on you with contempt.')
    giant.add_adjectives('massive', 'towering')
    giant.choices = [giant.attack_enemy]
    giant.set_combat_vars(5, 40, 60, 20)
    giant.hitpoints = 30
    giant.health = giant.hitpoints
    
    axe = gametools.clone('domains.centrata.key_quest.axe')
    giant.insert(axe)

    key = gametools.clone('domains.centrata.key_quest.key')
    key.qkey_number = 2
    giant.insert(key)
    return giant
