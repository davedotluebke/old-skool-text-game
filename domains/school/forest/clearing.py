import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    clearing = room.Room('clearing', pref_id=roomPath)
    clearing.set_description('bright clearing', 'This clearing is bright and has an absolutely enormous pile of random stuff in the centre of it.')
    clearing.add_adjectives('bright')
    clearing.add_exit('north', 'domains.school.forest.woods')

    # horster = gametools.clone('domains.school.forest.scavenger')
    # clearing.insert(horster)

    ruby = gametools.clone('domains.school.forest.ruby')
    clearing.insert(ruby)

    paper = gametools.clone('domains.school.forest.torn_paper')
    clearing.insert(paper)
    return clearing
