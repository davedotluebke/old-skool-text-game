from debug import dbg

from action import Action
from thing import Thing
from container import Container
from liquid import Liquid

class Cauldron(Container):
    recipes = [({'water', 'molasses'}, 'pink potion'),  #, 'poppyseed'
               ({'water', 'molasses', 'sunflower petal', 'cave moss', 'truffles'}, 'invisibilitypotion'),
               ({'poppyseed', 'truffles', 'cave moss'}, 'explode')]

    def __init__(self, default_name):
        super().__init__(default_name)
        self.liquid = True

    def insert(self, obj):
        if super().insert(obj): 
            return True
        for i in Cauldron.recipes:
            ingredients = {x.names[0] for x in self.contents}
            if i[0] == ingredients:  # set comparison
                if i[1] == 'explode':
                    self.explode()
                else:
                    for a in self.contents:
                        a.move_to(Thing.ID_dict['nulspace'])
                    created = Liquid(i[1])
                    created.set_description(i[1], 'This is %s %s' % ('an' if list(i[1])[1] in ['a','e','i','o','u'] else 'a', i[1]))
                    created.move_to(self)
                    self.emit('The contents of the cauldron simmer, smoke, then vanish with a bang! In their place a %s has formed.' % (created.short_desc))
        return False
    
    def explode(self):
        self.emit('The cauldron explodes with a bang, scattering broken glass and spilling its contents all over the floor')
        for i in self.contents:
            i.move_to(Thing.ID_dict['nulspace'])
        self.move_to(Thing.ID_dict['nulspace'])
        
