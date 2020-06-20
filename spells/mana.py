def get_mana(parser, cons, oDO, oIDO, spell_info, stone):
    return 0
def spell(parser, cons, oDO, oIDO, spell_info, stone):
    if not stone:
        cons.user.perceive('You have %s mana with a max of %s' % (cons.user.mana, cons.user.max_mana), force=True)
    else:
        cons.user.perceive('The %s has %s mana with a max of %s.' % (stone.get_short_desc(), stone.mana, stone.max_mana), force)True)
    return True
