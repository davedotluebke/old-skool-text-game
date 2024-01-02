# Adapted from domains/school/school/library_bookcase.py

import gametools
import random
from container import Container
from action import Action
from thing import Thing
from book import Book

class Bookshelf(Container):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, ID, path):
        super().__init__(ID, path)
        self.set_description('bookshelf full of books', 'This beautiful mahogany bookshelf is filled to the brim with books. ' \
        'Every time you look at it you notice another book.')
        self.fix_in_place("The bookshelf appears to be fixed to the wall.")
        self.books = [
            gametools.clone('domains.centrata.mansion.legal_advice_book')
        ]
        for i in range(0, len(self.books)):
            self.books.append(gametools.clone('domains.centrata.mansion.random_law_book'))
        
        for j in self.books:
            j.move_to(self, force_move=True)

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    #
    # SET/GET METHODS (methods to set or query attributes)
    #

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def look_at(self, p, cons, oDO, oIDO):
        """Look at the bookshelf, reading its description and listing some of the books. """
        result = Thing.look_at(self, p, cons, oDO, oIDO)
        if result != True:
            return result
        preamble = "%s the %s there is:" % (self.insert_prepositions[0], self.names[0])
        cons.write(preamble.capitalize())

        book_selection = []
        while len(book_selection) < 5:
            selected_book = random.choice(self.contents)
            if selected_book not in book_selection:
                book_selection.append(selected_book)
            if set(book_selection) == set(self.contents):
                break
        
        for item in book_selection:
            cons.write(item.get_short_desc(indefinite=True))
        return True
    
    actions = dict(Container.actions)
    actions['look'] =  Action(look_at, True, False)
    actions['examine'] = Action(look_at, True, False)

def clone():
    bookshelf = Bookshelf('bookshelf', __file__)
    return bookshelf
