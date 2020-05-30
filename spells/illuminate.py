import gametools
import random

def bad_spell(parser, cons, oDO, oIDO, spell_info, stone, how_badly):
    if how_badly < 0.2:
        duration = int(spell_info[0])/(3 * random.random() + 1)
        spell(parser, cons, oDO, oIDO, spell_info, stone, duration)
    elif how_badly < 0.8:
        cons.user.light = -1
        cons.user.emit('&nD%s starts drawing light into themself.' % cons.user)
        cons.user.perceive('You begin drawing light into yourself.')
        duration = int(spell_info[0])
        cons.game.schedule_event(duration, end_light_bad, cons)
        return True
    else:
        option = random.randint(0, 2)
        if option == 0:
            #take damage
            cons.user.take_damage(None, random.randint(0, 10))
        elif option == 1:
            #shame them
            cons.user.perceive('You have failed drastically at this spell. It paints a sorry picture for you future endeavors.', True)
        elif option == 2:
            #things fall out of their inventory
            num_items = random.randint(1, len(cons.user.contents))
            for i in range(0, num_items):
                item = random.choice(cons.user.contents)
                item.move_to(cons.user.location)
                cons.user.perceive('Your %s falls on the ground!' % item.get_short_desc())

def get_mana(parser, cons, oDO, oIDO, spell_info, stone):
    '''Get the mana amount required to cast this spell.'''
    try:
        mana = int(spell_info[0]) * 5
    except ValueError:
        raise gametools.BadSpellInfoError('Duration was not an integer!')
    except IndexError:
        raise gametools.BadSpellInfoError('You need to say how long you want to illuminate!')
    return mana

def end_light(cons):
    cons.user.emit('&nD%s stops glowing.' % cons.user)
    cons.user.perceive('You stop glowing.')
    cons.user.emits_light = False
    cons.user.light = 0

def end_light_bad(cons):
    cons.user.emit('&nD%s stops drawing light into themself.' % cons.user)
    cons.user.perceive('You stop draeing light into yourself.')
    cons.user.light = 0

def spell(parser, cons, oDO, oIDO, spell_info, stone, duration=None):
    '''Actually execute the spell.'''
    cons.user.emits_light = True
    cons.user.light = 1
    cons.user.emit('&nD%s begins glowing.' % cons.user)
    cons.user.perceive('You begin glowing.')
    if duration is None:
        duration = int(spell_info[0])
    cons.game.schedule_event(duration, end_light, cons)
    return True
