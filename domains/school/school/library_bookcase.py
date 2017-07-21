import domains.school.bookcase as bookcaseMod
import gametools

def clone():
    bookcase = bookcaseMod.Bookcase('bookcase', __file__, 'domains.school.school.potion_storage')
    return bookcase
