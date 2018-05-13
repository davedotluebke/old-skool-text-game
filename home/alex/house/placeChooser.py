from thing import Thing
from action import Action

class PlaceChooser(Thing):
    def __init__(self, ID, path):
        super().__init__(ID, path)
        self.written_on = 'domains.school.school.woods'
        self.actions.append(Action(self.write, ['write'], True, False))
        self.fix_in_place('This paper is fixed above the door with sorcery.')
        self.set_description('magical piece of paper', 'This magical paper says "domains.school.school.woods" on it.')
        self.add_names('paper')
        self.add_adjectives('magical')

    def write(self, p, cons, oDO, oIDO):
        try:
            self.written_on = " ".join(p.words[1:])
        except IndexError:
            return 'Did you mean to write something on the paper?'
        cons.write('You write "%s" on the paper and feel a magical shift occur.' % self.written_on)
        self.emit("&nD%s writes something on the paper and vanishes before your eyes!" % cons.user.id, cons.user)
        del self.location.exits['west']
        try:
            self.location.exits['west'] = self.written_on
            gametools.load_room(self.written_on)
        except KeyError:
            cons.write('The text on the paper morphs back into the word "woods".')
            self.written_on = 'domain.school.school.woods'
            self.location.exits['west'] = Thing.ID_dict[self.written_on]
        self.long_desc = 'This magical paper says "%s" on it.' % self.written_on
        return True

def clone():
    paper = PlaceChooser('paper', __file__)
    return paper