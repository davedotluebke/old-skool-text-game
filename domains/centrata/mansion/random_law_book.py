import random
import book
from action import Action

legal_journals = ["The Centrata Review of Law", "A Legal Primer: Centrata", "Centrata Courts Review"]

class RandomLawBook(book.Book):
    def __init__(self):
        volume_number = random.randint(1, 255)
        issue_number = random.randint(1, 12)

        legal_journal = random.choice(legal_journals)

        self.book_title = f"{legal_journal}: Volume {volume_number}, Issue {issue_number}"

        self.book_msg = """
    \=============================================
    %s
    \=============================================""" % self.book_title
        
        self.book_msg += random.randint(1, 200) * "This page is extremely boring and technical."

        book_adjectives = random.choice(["heavy", "light"])
        super().__init__('book', __file__, f'{book_adjectives} brown book', f'This is a {book_adjectives} brown book titled {self.book_title}')
        self.add_adjectives(*book_adjectives)
        self.set_message(self.book_msg)

def clone():
    return RandomLawBook()

