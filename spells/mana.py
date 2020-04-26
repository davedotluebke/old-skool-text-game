def get_mana(parser, cons, oDO, oIDO, spell_info):
    return 0
def spell(parser, cons, oDO, oIDO, spell_info):
    cons.write('You have %s mana with a max of %s' % (cons.user.mana, cons.user.max_mana))
    return True