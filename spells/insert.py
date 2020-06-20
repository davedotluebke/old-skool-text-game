import gametools

def get_mana(parser, cons, oDO, oIDO, spell_info, stone):
    return 0
def spell(parser, cons, oDO, oIDO, spell_info, stone):
    if not stone:
        cons.user.perceive('I don\'t know what stone you want to put mana into!', force=True)
    else:
        try:
            mana = int(spell_info[0])
        except:
            raise gametools.BadSpellInfoError('You nned to specify how much mana to insert!')
        if cons.user.mana >= mana:
            if not stone.set_mana(stone.get_mana()+mana):
                cons.user.perceive('You are trying to put more mana into the stone than its max.', force=True)
            else:
                cons.user.set_mana(cons.user.mana-mana)
                cons.user.perceive('The %s now has %s mana with a max of %s.' % (stone.get_short_desc(), stone.mana, stone.max_mana), force=True)
        else: 
            cons.user.perceive('You are trying to put more mana into the stone than you have!', force=True)
    return True