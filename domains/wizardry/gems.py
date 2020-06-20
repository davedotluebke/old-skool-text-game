from stones import *

# this file is maintained for backwards compatibility. See stones.py for the newer syntax
class Gem(Stone):
    def __init__(self, path, default_name, short_desc, long_desc, power_num=10, pref_id=None):
        super().__init__(default_name, path, mana=power_num, max_mana=power_num)
        self.set_description(short_desc, long_desc)
        self.log.warning('This is deprecated. Use stones.Stone instead.')

Emerald = Gem
Ruby = Gem
Jade = Gem
Diamond = Gem
Opal = Gem
Pearl = Gem
