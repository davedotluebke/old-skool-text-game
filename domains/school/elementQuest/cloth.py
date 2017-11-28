import thing
import action
import gametools

class FireQuestCloth(thing.Thing):
    def wrap(self, p, cons, oDO, oIDO):
        if not oIDO:
            return "Did you mean to wrap the cloth around something?"
        if oIDO.names[0] != 'branch':
            cons.write('You wrap the cloth around the %s, but it falls off.' % oIDO.short_desc)
            return True
        cons.user.perceive('You wrap the cloth around the branch, creating a makeshift torch.')
        torch = gametools.clone('domains.school.elementQuest.torch')
        torch.soaked = oDO.soaked
        torch.move_to(oIDO.location)
        for i in [oDO, oIDO]:
            i.move_to(thing.Thing.ID_dict['nulspace'])
        return True

def clone():
    cloth = FireQuestCloth('torn tapestry', __file__, pref_id="torn_tapestry")
    cloth.set_description('torn bit of tapestry', 'This is a torn swath of tapestry, strewn on the ground. It doesn\'t seem to match any of the tapestries hanging in any rooms you have seen.')
    cloth.add_adjectives('torn')
    cloth.add_names('tapestry', 'swath', 'cloth')
    cloth.actions.append(action.Action(cloth.wrap, ['wrap'], True, False))
    cloth.soaked = False
    return cloth
