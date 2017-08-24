import thing
import gametools

def wrap(p, cons, oDO, oIDO):
    if oDO.path != 'domains.school.elementQuest.cloth':
        return "Did you mean to wrap the cloth around something?"
    if oIDO.path != 'domains.school.elementQuest.branch':
        cons.write('You wrap the cloth around the %s, and it falls off.' % oIDO.short_desc)
        return True
    cons.write('You wrap the cloth around the branch and create a torch.')
    torch = gametools.clone('domains.school.elementQuest.torch')
    torch.move_to(oIDO.location)
    for i in [oDO, oIDO]:
        i.move_to(thing.Thing.ID_dict['nulspace'])
    return True

def clone():
    cloth = thing.Thing('cloth', __file__)
    cloth.set_description('plain white cloth', 'This cloth is plain white. It is very thin.')
    cloth.add_adjectives('plain', 'white')
    cloth.actions.append(thing.Action(wrap, ['wrap'], True, False))
    return cloth
