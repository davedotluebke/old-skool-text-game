import gametools

def get_mana(parser, cons, oDO, oIDO, spell_info, stone):
    return 0
def spell(parser, cons, oDO, oIDO, spell_info, stone):
    if not stone:
        cons.write('I don\'t know what stone you want to put mana into!')
    else:
        try:
            mana = int(spell_info[0])
        except:
            raise gametools.BadSpellInfoError('You nned to specify how much mana to insert!')
        if cons.user.mana >= mana:
            if not stone.set_mana(stone.get_mana()+mana):
                cons.write('You are trying to put more mana into the stone than its max.')
            else:
                cons.user.set_mana(cons.user.mana-mana)
                cons.write('The %s now has %s mana with a max of %s.' % (stone.get_short_desc(), stone.mana, stone.max_mana))
        else: 
            cons.write('You are trying to put more mana into the stone than you have!')
    return True