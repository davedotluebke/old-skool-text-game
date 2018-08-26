from thing import Thing
import gametools

class Plurality(Thing):
    def __init__(self, source, count):
        '''Create a plurality of <source>, containing <count> objects. 
        <source> is a Thing and <count> is an integer greater than 2.'''
        self.cononical = source
        self.spare = copy(source)

        Thing.ID_dict[self.cononical.id] = self

        self.cononical.id = None
        self.spare.id = None
        raise NotImplementedError("have not finished")

    def check_if_identical(self, obj1, obj2):
        '''Check if two objects are identical for the 
        purpose of putting them in a plurality.'''
        raise NotImplementedError("needs work")

# overloaded by the plurality:
# - __init__
# - get_savable
# - restore_objs_from_IDs
# - change_objs_to_IDs
# - set_weight
# - set_volume
# - fix_in_place
# - set_description
# - take
# - drop
# - look_at