import container

class Chandelier(container.Container):
    def insert(self, obj, force_insert=False, merge_pluralities=True):
        result = super().insert(obj, force_insert, merge_pluralities)
        if result: # reminder, insert() returns True if insert failed
            # chandelier comes crashing down
            pass
        return result

def clone():
    chandelier = Chandelier('chandelier', __file__)
    chandelier.set_description('rose-tinted chandelier', 'This low-hanging chandelier is shimmering in brilliant rose colours that reflect throughout the entire room.', unlisted=True)
    chandelier.closable = False
    chandelier.add_adjectives('rose', 'tinted', 'rose-tinted', 'low', 'hanging', 'low-hanging', 'shimmering')
    chandelier.set_prepositions('on', 'onto')
    chandelier.fix_in_place('The chandelier is attached to the ceiling.')
    
    return chandelier
