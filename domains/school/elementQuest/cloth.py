import thing
import gametools

class FireQuestCloth(thing.Thing):
    def wrap(p, cons, oDO, oIDO):
        if oDO != self:
            return "Did you mean to wrap the cloth around something?"
        if oIDO.names[0] != 'branch':
            cons.write('You wrap the cloth around the %s, and it falls off.' % oIDO.short_desc)
            return True
        cons.write('You wrap the cloth around the branch and create a torch.')
        torch = gametools.clone('domains.school.elementQuest.torch')
        torch.soaked = oDO.soaked
        torch.move_to(oIDO.location)
        for i in [oDO, oIDO]:
            i.move_to(thing.Thing.ID_dict['nulspace'])
        return True

def clone():
    cloth = FireQuestCloth('torn tapestry', __file__)
    cloth.set_description('torn bit of tapestry', 'This is a torn swath of tapestry, strewn on the ground. It doesn\'t seem to match any of the tapestries hanging in any rooms you have seen.')
    cloth.add_adjectives('torn')
    cloth.add_names('tapestry', 'swath')
    cloth.actions.append(thing.Action(cloth.wrap, ['wrap'], True, False))
    cloth.soaked = False
    return cloth
