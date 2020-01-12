# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

def load(param_list):
    path = param_list[0] # if paramaters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists
    
    road_start = param_list[1]
    road_end = param_list[2]
    road_length = int(param_list[3])
    road_section = int(param_list[4])

    this_road = room.Room('road', path)

    random.seed(road_section*road_length)

    description_map = {'mountains':['tall', 'steep', 'magnificent', 'large', 'distant'],
                       'forests':  ['pine','evergreen', 'thick', 'dense', 'sparse', 'dead'],
                       'woods':    ['light', 'open', 'thin', 'thick'],
                       'hills':    ['small', 'larger', 'wooded', 'grassy'],
                       'plains':   ['wide', 'huge', 'empty'],
                       'praries':  ['tall', 'brown-grassed', 'dry'],
                       'swamps':   ['deep', 'wooden', 'wet', 'huge', 'small'],
                       'lakes':    ['deep', 'frozen', 'huge', 'small']}

    noun1 = random.choice(list(description_map))
    noun2 = random.choice(list(description_map))

    west_side = 'some %s %s' % (random.choice(description_map[noun1]), noun1)
    east_side = 'some %s %s' % (random.choice(description_map[noun2]), noun2)

    this_road.set_description('streach of road', 'This stretch of road (section %s) continues north and south. On the east side of the road, you see %s. On the west side of the road, you see %s.' % (road_section, west_side, east_side))

    if road_section == 0:
        this_road.add_exit('south', road_start)
    else:
        this_road.add_exit('south', 'domains.centrata.kings_road?%s&%s&%s&%s' % (road_start, road_end, road_length, str(road_section-1)))

    if road_section == road_length - 1:
        this_road.add_exit('north', road_end)
    else:
        this_road.add_exit('north', 'domains.centrata.kings_road?%s&%s&%s&%s' % (road_start, road_end, road_length, str(road_section+1)))

    return this_road
