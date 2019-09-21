from debug import dbg

from thing import Thing
from container import Container
from potions import PinkPotion
from potions import InvisibilityPotion
from potions import StrengthPotion
import gametools

class Cauldron(Container):
    # Explanation: tuple of 2 items: set of ingredients and string name of potion file (spaces automatically replaced with underscores)
    recipes = [({'water', 'molasses', 'poppyseed'}, 'pink potion'),  
               ({'water', 'molasses', 'sunflower petal', 'cave moss', 'truffles'}, 'invisibility potion'),
               ({'poppyseed', 'truffles', 'cave moss'}, 'explode'),
               ({'molasses', 'dragon scale', 'poppyseed'}, 'strength potion'),
               ({'spring', 'hay', 'dragon scale'}, 'jumping potion'),
               ({'dragon scale', 'poppyseed', 'spring'}, 'explode'),
               ({'dragon scale', 'truffles', 'molasses'}, 'exploration potion')]

    def __init__(self, default_name, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.liquid = True
        self.versions[gametools.findGamePath(__file__)] = 1

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    #
    # SET/GET METHODS (methods to set or query attributes)
    #

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def insert(self, obj, force_insert=False):
        if super().insert(obj, force_insert): 
            return True
        for i in Cauldron.recipes:
            ingredients = {x.names[0] for x in self.contents}
            if i[0] == ingredients:  # set comparison
                if i[1] == 'explode':
                    Thing.game.events.schedule(Thing.game.time+1, self.explode)
                else:
                    Thing.game.events.schedule(Thing.game.time+3, self.create_potion, i)
        return False
    
    def explode(self, none=None):
        self.emit('The cauldron explodes with a bang, scattering broken glass and spilling its contents all over the floor')
        for i in self.contents:
            i.move_to(Thing.ID_dict['nulspace'])
        self.move_to(Thing.ID_dict['nulspace'])

    def create_potion(self, i):
        while self.contents:
            a = self.contents[0]
            self.extract(a)
            Thing.ID_dict['nulspace'].insert(a)
        try:
            created = gametools.clone(i[1].replace(' ', '_'))
            created.move_to(self)
        except FileNotFoundError:
            dbg.debug('Error! Cauldron recipies dictionary called for the creation of %s, but no file was found!')
        self.emit('The contents of the cauldron simmer, smoke, then vanish with a bang! In their place a %s has formed.' % (created.get_short_desc()))
        
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
