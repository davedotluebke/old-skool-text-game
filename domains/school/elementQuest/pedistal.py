import container
import creature
import action

class Pedistal(container.Container):
    def __init__(self):
        super().__init__('pedistal', __file__)
        self.set_description('pedistal', 'This is a large pedistal in the centre of the room. It has a strangely shaped triangular space on it.', unlisted=True)
        self.add_adjectives('strange', 'large', 'central', 'stangely', 'shaped', 'centre')
        self.fix_in_place('The pedistal is attached to the floor.')
        self.set_prepositions('on', 'onto', 'atop')

    def put(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if oDO == None or oIDO == None:
            return "What are you trying to put %s what? " % sPrep
        if oIDO != self:
            return "Did you mean to 'put' something %s the %s?" % (sPrep, self._short_desc)
        if oDO.fixed: return oDO.fixed
        if sPrep not in self.insert_prepositions:
            return "You can't put the %s %s the %s, but you can put it %s the %s." % (oDO, sPrep, self, self.insert_prepositions[0], self)
        if self.closed:
            cons.user.perceive(self.closed_err if self.closed_err else "The %s is closed; you can't put anything %s it." % (self._short_desc, self.insert_prepositions[0]))
            return True
        if 'prism' in oDO.names:
            cons.user.perceive('You put the prism onto the pedistal. It slides into the space and is suddenly illuminated by the sun, '
            'creating a rainbow to the west. Strangely, the rainbow now seems to be projected onto a solid stone bridge.')
            self.emit(f'&nD{cons.user.id} puts the prism onto the pedistal. It slides into the space and is suddenly illuminated by the sun, '
            'creating a rainbow to the west. Strangely, the rainbow now seems to be projected onto a solid stone bridge.')
            self._long_desc = 'This is a large pedistal in the centre of the room. It has a prism on it.'
            oDO.move_to(self)
            oDO.fix_in_place('The prism seems attached to the pedistal.')
            oDO.unlisted = True
            self.location.add_exit('west','domains.school.elementQuest.bridge')
            self.location.set_description('walkway', 'This walkway leads west from the tower and onto a bridge to the west.')
            return True
        else:
            cons.user.perceive(f'Despite your best attempts to put the {oDO.name()} on the pedistal, it will not stay there for some reason.')
            self.emit(f'&nD{cons.user.id} tries to put the {oDO.name()} on the pedistal, but eventually gives up.')
            return True
    
    actions = dict(container.Container.actions)
    actions['put'] = action.Action(put, True, False)

def clone():
    return Pedistal()
