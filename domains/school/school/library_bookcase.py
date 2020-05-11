import gametools
import random
from container import Container
from action import Action
from thing import Thing
from book import Book       

class Bookcase(Container):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, ID, path):
        super().__init__(ID, path)
        self.set_description('bookcase full of books', 'This bookcase is a hodgepodge of books; some are newer, but a lot of old ones are scattered around them. '
        'Every time you look at it you notice another book.')
        self.fix_in_place("The bookcase appears to be fixed to the wall.")
        self.door_open = False
        self.books = [
            gametools.clone('domains.school.school.potion_book'),
            gametools.clone('domains.school.school.blue_book'),
            gametools.clone('domains.school.school.secret_passage_book')
        ]
        for i in range(0, len(self.books)):
            self.books.append(gametools.clone('domains.school.school.random_book'))
        
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
    
    def close_action(self, p, cons, oDO, oIDO):
        if not self.door_open:
            return super().close_action(p, cons, oDO, oIDO)
        cons.user.perceive('You close the bookcase door.')
        self.emit('&nD%s closes the bookcase door.' % cons.user.id)
        self.set_description('bookcase full of books', 'This bookcase is a hodgepodge of books; some are newer, but a lot of old ones are scattered around them. '
        'Every time you look at it you notice another book.')
        del self.location.exits['down']
        self.door_open = False
        return True
    
    actions = dict(Container.actions)
    actions['look'] =  Action(look_at, True, False)
    actions['examine'] = Action(look_at, True, False)
    actions['close'] = Action(close_action, True, False)

def clone():
    bookcase = Bookcase('bookcase', __file__)
    return bookcase
