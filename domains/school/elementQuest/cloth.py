import thing
import action
import gametools

class FireQuestCloth(thing.Thing):
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def wrap(self, p, cons, oDO, oIDO):
        if not oIDO:
            return "Did you mean to wrap the cloth around something?"
        if oIDO.names[0] != 'branch':
            cons.write('You wrap the cloth around the %s, but it falls off.' % oIDO._short_desc)
            return True
        cons.user.perceive('You wrap the cloth around the branch, creating a makeshift torch.')
        torch = gametools.clone('domains.school.elementQuest.torch')
        torch.soaked = oDO.soaked
        torch.move_to(oIDO.location)
        for i in [oDO, oIDO]:
            i.move_to(thing.Thing.ID_dict['nulspace'])
        return True

    actions = dict(Thing.actions)  # make a copy, don't change Thing's dict!
    actions['wrap'] = Action(wrap, True, False)
    
#
# MODULE-LEVEL FUNCTIONS (e.g., clone())
#
def clone():
    cloth = FireQuestCloth('torn tapestry', __file__, pref_id="torn_tapestry")
    cloth.set_description('torn bit of tapestry', 'This is a torn swath of tapestry, strewn on the ground. It doesn\'t seem to match any of the tapestries hanging in any rooms you have seen.')
    cloth.add_adjectives('torn')
    cloth.add_names('tapestry', 'swath', 'cloth')
    cloth.soaked = False
    return cloth
