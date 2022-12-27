import gametools
import random
import creature

def get_mana(parser, cons, oDO, oIDO, spell_info, stone):
    '''Get the mana amount used to cast this spell.'''
    try:
        mana = int(spell_info[-1]) * 20
    except ValueError:
        raise gametools.BadSpellInfoError('Healing amount was not an integer!')
    except IndexError:
        raise gametools.BadSpellInfoError('You need to say how much health you want to restore to who!')
    return mana

def spell(parser, cons, oDO, oIDO, spell_info, stone, duration=None):
    '''Actually execute the spell.'''
    (sV, sDO, sPrep, sIDO) = parser.diagram_sentence(parser.words)

    target = oIDO if oIDO else oDO
    if not target and len(parser.words) > 2 and parser.words[2] == 'myself':
        target = cons.user

    if not target:
        if sIDO:
            target_text = ' '.join(sIDO.split(" ")[0:-1])
            matches = parser.find_matching_objects(target_text, parser._collect_possible_objects(cons.user, not sV in parser.environment_verbs, not sV in parser.inventory_verbs), cons)
            if matches:
                target = matches[0]
    
    if not isinstance(target, creature.Creature):
        return "I'm not sure who you're trying to heal!"
    new_health = target.health + int(spell_info[-1])
    if new_health > target.hitpoints: # new health can't be above max
        new_health = target.hitpoints
    
    target.health = new_health

    if target == cons.user:
        cons.user.perceive("You feel yourself suddenly rejuvinated.")
        return True
    
    cons.user.emit('A streak of warm light shoots from &nd%s to &nd%s.' % (cons.user, target), ignore=[cons.user, target])
    cons.user.perceive('A streak of warm light shoots from you to &nd%s.' % target)
    target.perceive('A streak of warm light shoots from &nd%s to you, and you feel yourself suddenly rejuvinated.' % cons.user)
    return True
    