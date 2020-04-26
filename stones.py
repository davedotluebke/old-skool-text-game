from thing import Thing
from action import Action
import gametools

class Stone(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, mana, max_mana):
        super().__init__(default_name, path)
        self.mana = mana
        self.max_mana = max_mana
    #
    # SET/GET METHODS (methods to set or query attributes)
    #
    def get_mana(self, attr='both'):
        if attr == 'mana':
            return self.mana
        elif attr in ['max', 'max_mana']:
            return self.max_mana
        else:
            return self.mana, self.max_mana
    def set_mana(self, mana):
        try:
            intmana = int(mana)
            if intmana != mana:
                self.log.warning('Converted mana to integer')
            if mana >= 0:
                self.mana = intmana
            else:
                self.log.error('Mana must be non-negative')
        except TypeError:
            self.log.error('Mana must be a non-negative integer')
    def set_max_mana(self, mana):
        try:
            intmana = int(mana)
            if intmana != mana:
                self.log.warning('Converted max_mana to integer')
            if mana >= 0:
                self.mana = intmana
            else:
                self.log.error('Mana must be non-negative')
        except TypeError:
            self.log.error('Mana must be a non-negative integer')