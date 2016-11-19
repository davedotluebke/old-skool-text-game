from debug import dbg
from player import Player
from parse import Parser


class Console:
    def __init__(self):
        self.parser = Parser()
 
    def set_user(self, cons_user):
        """Set the Player object associated with this console."""
        self.user = cons_user
        
    def write(self, text):
        print(text)

    def loop(self, user, g):
        print('\n')
        dbg.debug('This is not a valid function anymore.')

    def take_input(self, prompt):
        return input(prompt)
        dbg.debug(self)

