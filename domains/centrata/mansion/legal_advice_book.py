import book

def clone():
    legal_advice_book = book.Book('book', __file__, 'heavy old book', 'This is a heavy old book titled "Legal Advice for Centrata".')
    legal_advice_book.add_adjectives('heavy', 'old')
    legal_advice_book.set_message('''
    |=========================|
    |Legal Advice for Centrata|
    |=========================|
    #*
    Chapter 1: The King and his Court
    Chapter 2: Parliament and its role
    Chapter 3: The Criminal Code
    Chapter 4: Your rights if accused of a crime
    Chapter 5: Additional information
    #*
    This page is badly stained and cannot be made out.
    ''')
    return legal_advice_book
