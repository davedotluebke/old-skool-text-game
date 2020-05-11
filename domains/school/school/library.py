import gametools
import room

from domains.school.school.library_book import LibraryBook

from scenery import Scenery
from action import Action

class LibraryRoom(room.Room):
    def go_to(self, p, cons, oDO, oIDO):
        for i in list(cons.user.contents):
            if isinstance(i, LibraryBook):
                cons.user.perceive('&nD%s disappears with a flash and reappears on the bookshelf.' % i.id)
                i.move_to(self.bookcase)
        return super().go_to(p, cons, oDO, oIDO)

    actions = dict(room.Room.actions)
    actions['go'] = Action(go_to, True, False)
    actions['walk'] = Action(go_to, True, False)

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    library = LibraryRoom('library', safe=True, pref_id=roomPath)
    library.indoor = True
    library.set_description('library', "You find yourself in a comfortable library filled from floor to ceiling with books and bookcases. The room is circular and must be built into a round tower as windows look out in every direction. A spiral staircase in the centre of the room leads upwards.")
    library.add_exit('northwest', 'domains.school.school.landing')
    library.add_exit('up', 'domains.school.school.towerstairs')
    library.add_exit('southwest', 'domains.school.school.arena')

    bookcase = gametools.clone('domains.school.school.library_bookcase')
    library.bookcase = bookcase
    library.insert(bookcase)

    return library
