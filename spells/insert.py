def get_mana(parser, cons, oDO, oIDO, spell_info, stone):
    return 0
def spell(parser, cons, oDO, oIDO, spell_info, stone):
    if not stone:
        cons.write('I don\'t know what stone you want to put mana into!')
    else:
        mana = spell_info[0]
        if cons.user.mana >= mana:
            stone.set_mana(stone.get_mana()+mana)
            cons.user.set_mana(cons.user.mana-mana)
            cons.write('The %s has %s mana with a max of %s.' % (stone.get_short_desc(), stone.mana, stone.max_mana))
        else: 
            cons.write('You are trying to put more mana into the stone than you have!'
    return True