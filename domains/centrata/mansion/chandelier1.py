import container

class Chandelier(container.Container):
    def insert(self, obj, force_insert=False, merge_pluralities=True):
        result = super().insert(obj, force_insert, merge_pluralities)
        if result: # reminder, insert() returns True if insert failed
            # chandelier comes crashing down
            self.emit('The chandelier crashes down to the ground!')
            self.set_description('shattered rose-tinted chandelier', 'This chandelier sits on the floor, shattered rose-tinted glass across everywhere.')
            self.add_adjectives('shattered')
            self.fix_in_place('The shattered chandelier is far too heavy - and sharp - to move.')
            self.set_max_weight_carried(4e9)
        return result
    
    def climb(self, p, cons, oDO, oIDO):
        if oDO != self and oIDO != self:
            return "Did you mean to climb on the chandelier?"
        
        # chandelier comes crashing down
        self.emit('The chandelier crashes down to the ground!')
        self.set_description('shattered rose-tinted chandelier', 'This chandelier sits on the floor, shattered rose-tinted glass across everywhere.')
        self.add_adjectives('shattered')
        self.fix_in_place('The shattered chandelier is far too heavy - and sharp - to move.')
        self.set_max_weight_carried(4e9)
        
    actions = dict(container.Container.actions)
    actions['climb'] = container.Action(climb, True, False)

def clone():
    chandelier = Chandelier('chandelier', __file__)
    chandelier.set_description('rose-tinted chandelier', 'This low-hanging chandelier is shimmering in brilliant rose colours that reflect throughout the entire room.')
    chandelier.closable = False
    chandelier.add_adjectives('rose', 'tinted', 'rose-tinted', 'low', 'hanging', 'low-hanging', 'shimmering')
    chandelier.set_prepositions('on', 'onto')
    chandelier.fix_in_place('The chandelier is attached to the ceiling.')
    
    chandelier.set_max_volume_carried(100)
    chandelier.set_max_weight_carried(5000)
    
    return chandelier
