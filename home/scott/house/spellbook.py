import book

def clone():
    spellbook = book.Book("spellbook", __file__, "hard-covered spellbook", "This spellbook has a very sturdy cover.")
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
    Mana: self.mana, self.max_mana
    Illuminate: self.light
    Insert: add stuff to emerald
    ''')
    return spellbook
