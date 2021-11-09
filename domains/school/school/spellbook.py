import book
import domains.school.school.library_book as library_book

def clone():
    spellbook = library_book.LibraryBook("spellbook", __file__, "hard-covered spellbook", "This spellbook has a very sturdy cover.")
    spellbook.add_names("book")
    spellbook.add_adjectives("sturdy", "hard-covered", "spell")
    spellbook.set_message('''
    \\==================
    |     Spells     |
    \\==================
    #*
    Spells: pg 1-end
    #*
    \0{"mana": "spells.mana", "illuminate": "spells.illuminate", "insert": "spells.insert"}
    Mana: This spell allows you to check how much mana you have to cast more spells. To cast 
    spells, type "cast". To learn spells, type "learn" followed by the spell you want to learn.
    Illuminate: This spell allows you to bring light to the world. 
    Insert: This spell allows you to fill gems with your mana for future use.
    ''')
    return spellbook