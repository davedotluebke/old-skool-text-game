import gametools
import domains.school.school.library_book as library_book
import action

class SecretPassageBook(library_book.LibraryBook):
    def __init__(self):
        super().__init__('book', __file__, 'tattered old book', 'This book looks extremely tattered, even more so than any of the other books on the shelf.')
        self.add_adjectives('tattered', 'old')
        self.hidden_room = 'domains.school.school.potion_storage'
        self.fix_in_place('This book is secretly hooked to the shelf. ')
    
    def take(self, p, cons, oDO, oIDO):
        cons.user.perceive('You pull on a book. ')
        self.emit("&nD%s does something to the bookcase." % cons.user.id)
        cons.user.perceive('The bookcase shakes, and swings open, revealing a secret staircase leading down.')
        self.emit('The bookcase shakes, and swings open, revealing a secret staircase leading down.')
        self.location.location.add_exit('down', self.hidden_room)
        self.location.set_description('bookcase door wide open to a secret staircase', 'This door is cleverly disguised as a bookcase. It is open, revealing a secret staircase leading down.')
        self.location.door_open = True
        return True
    
    actions = dict(library_book.LibraryBook.actions)
    actions['take'] = action.Action(take, True, False)
    actions['get'] =  action.Action(take, True, False)

def clone():
    return SecretPassageBook()