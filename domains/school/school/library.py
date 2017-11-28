import gametools
import room

from book import Book

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    library = room.Room('library', safe=True, pref_id=roomPath)
    library.indoor = True
    library.set_description('library', "You find yourself in a comfortable library filled from floor to ceiling with books and bookcases. The room is circular and must be built into a round tower as windows look out in every direction. A spiral staircase in the center of the room leads upwards.")
    library.add_exit('northwest', 'domains.school.school.landing')
    library.add_exit('up', 'domains.school.school.towerstairs')

    bookcase = gametools.clone('domains.school.school.library_bookcase')
    library.insert(bookcase)

    potion_book = gametools.clone('domains.school.school.potion_book')
    library.insert(potion_book)

    blue_book = gametools.clone('domains.school.school.blue_book')
    library.insert(blue_book)

    return library
