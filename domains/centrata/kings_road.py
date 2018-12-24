# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

def load(param_list):
    path = param_list[0] # if paramaters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists
    
    road_section = int(param_list[1])

    this_road = room.Room('road', path)

    random.seed(road_section)

    nouns = ['mountains', 'forests', 'woods', 'hills', 'plains', 'praries', 'grasslands', 'swamps', 'lakes']
    adjectives = ['woody', 'gorgeous', 'historic', 'dense', 'open', 'tall', 'short', 'deep', 'frozen']

    west_side = 'some %s %s' % (random.choice(adjectives), random.choice(nouns))
    east_side = 'some %s %s' % (random.choice(adjectives), random.choice(nouns))

    this_road.set_description('streach of road', 'This stretch of road (section %s) continues north and south. On the east side of the road, you see %s. On the west side of the road, you see %s.' % (road_section, west_side, east_side))

    this_road.add_exit('north', 'domains.centrata.kings_road?%s' % str(road_section+1))

    if road_section > 0:
        this_road.add_exit('south', 'domains.centrata.kings_road?%s' % str(road_section-1))
    else:
        this_road.add_exit('south', 'domains.centrata.firefile_area.fields.road_four')

    return this_road
