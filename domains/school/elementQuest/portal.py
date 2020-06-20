import thing
import player
import action
import gametools

class Portal(thing.Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('portal', __file__)
        self.set_description('portal', 'This ancient portal is made of three vast stones, each covered '
                             'with arcane runes. A vertical sheet of glowing flame roars between the '
                             'stones, filling the portal with an inferno of powerful magic fire.')
        self.add_adjectives('flaming', 'stone')
        self.fix_in_place('You can\'t move the portal!')

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def enter(self, p, cons, oDO, oIDO):
        if oDO == self:
            cons.user.wizardry_element = 'fire'
            cons.user.complete_quest('Complete a quest to find thy element')
            cons.user.perceive('You steel yourself and step through the flaming portal. Oddly, the '
                               'roaring flames do not burn, but instead the fire fills you with a '
                               'tingling warmth. The flames surround you and suddenly disappear as '
                               'if your body had extinguished--no, ABSORBED--the fire.  You suddenly '
                               'realize you are in a different place...')
            lounge = gametools.load_room('domains.school.school.fire_lounge')
            if lounge and cons.user.move_to(lounge):
                    self.emit('&nD%s enters the fiery portal, and disappears in a burst of flame!', cons.user.id)
            else:
                cons.user.perceive('...and just as quickly, you feel yourself return! But something has changed...')
            return True
        return "Did you mean to enter the portal?"

    actions = dict(thing.Thing.actions)
    actions['enter'] = action.Action(enter, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    return Portal()