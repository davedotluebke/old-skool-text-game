import container
import gametools

def clone():
    bookshelf = container.Container('bookshelf', __file__)
    bookshelf.set_description('oak bookshelf', 'This bookshelf is made of oak. It has many different books on it.')
    bookshelf.closable = False
    bookshelf.add_adjectives('oak')
    bookshelf.add_names('shelf')
    bookshelf.set_prepositions('on', 'onto')

    blue_book = gametools.clone('home.alex.house.blue_book')
    blue_book.move_to(bookshelf, True)

    dusty_book = gametools.clone('home.alex.house.dusty_book')
    dusty_book.move_to(bookshelf, True)
    return bookshelf
