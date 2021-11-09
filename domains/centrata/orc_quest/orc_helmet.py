import thing

def clone(): 
    helmet = thing.Thing('helmet', __file__)
    helmet.set_description('crested helmet', 'This helmet is made of some '
        'golden-hued metal and encrusted with semi-precious stones. It is '
        'topped with a tall fluted crest.')
    helmet.add_adjectives('crested', 'golden', 'gold', 'golden-hued')
    helmet.orc_quest = True  # unique attribute to verify this for the quest
    return helmet
