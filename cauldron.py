from debug import dbg

from action import Action
from thing import Thing
from container import Container
from potions import PinkPotion
from potions import InvisibilityPotion
from potions import StrengthPotion
import gametools

class Cauldron(Container):
    recipes = [({'water', 'molasses', 'poppyseed'}, 'pink potion'),  
               ({'water', 'molasses', 'sunflower petal', 'cave moss', 'truffles'}, 'invisibility potion'),
               ({'poppyseed', 'truffles', 'cave moss'}, 'explode'),
               ({'molasses', 'dragon scale', 'poppyseed'}, 'strength potion')]

    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
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
                    if i[1] == 'pink potion':
                        created = PinkPotion(i[1])
                        created.set_description(i[1], 'This is %s %s' % ('an' if list(i[1])[0] in ['a','e','i','o','u'] else 'a', i[1]))
                        created.add_names('potion')
                        created.move_to(self)
                    if i[1] == 'invisibility potion':
                        created = gametools.clone('invisibility_potion')
                        created.move_to(self)
                    if i[1] == 'strength potion':
                        created = StrengthPotion(i[1])
                        created.set_description(i[1], 'This is %s %s' % ('an' if list(i[1])[0] in ['a','e','i','o','u'] else 'a', i[1]))
                        created.move_to(self)
                        created.add_names('potion')
                    self.emit('The contents of the cauldron simmer, smoke, then vanish with a bang! In their place a %s has formed.' % (created.short_desc))
        return False
    
    def explode(self):
        self.emit('The cauldron explodes with a bang, scattering broken glass and spilling its contents all over the floor')
        for i in self.contents:
            i.move_to(Thing.ID_dict['nulspace'])
        self.move_to(Thing.ID_dict['nulspace'])
        
