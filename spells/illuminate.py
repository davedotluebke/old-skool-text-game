import gametools

def get_mana(parser, cons, oDO, oIDO, spell_info):
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

def spell(parser, cons, oDO, oIDO, spell_info):
    '''Actually execute the spell.'''
    cons.user.emits_light = True
    cons.user.light = 1
    cons.user.emit('&nD%s begins glowing.' % cons.user)
    cons.user.perceive('You begin glowing.')
    duration = int(spell_info[0])
    cons.game.schedule_event(duration, end_light, cons)
    return True
