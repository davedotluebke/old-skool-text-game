import container

def clone():
    chandelier = container.Container('chandelier', __file__)
    chandelier.set_description('rose-tinted chandelier', 'This low-hanging chandelier is shimmering in brilliant rose colours that reflect throughout the entire room.', unlisted=True)
    chandelier.closable = False
    chandelier.add_adjectives('rose', 'tinted', 'rose-tinted', 'low', 'hanging', 'low-hanging', 'shimmering')
    chandelier.set_prepositions('on', 'onto')
    
    return chandelier
