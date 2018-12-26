# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

def load(param_list):
    path = param_list[0] # if paramaters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists
    
    coords = [int(param_list[1]), int(param_list[2]), int(param_list[3])]

    this_room = room.Room('cave', path)

    for i in ['north', 'south', 'east', 'west', 'up', 'down']:
        t_add_exit = True
        if i == 'north':
            r_seed = (coords[0]*coords[1]*coords[2]*(coords[0]+1)*coords[1]*coords[2])
            if r_seed == 0:
                r_seed = (coords[0]+coords[1]+coords[2]+(coords[0]+1)+coords[1]+coords[2])
            random.seed(r_seed)
            loc_string = 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (coords[0]+1, coords[1], coords[2])
        elif i == 'south':
            r_seed = (coords[0]*coords[1]*coords[2]*(coords[0]-1)*coords[1]*coords[2])
            if r_seed == 0:
                r_seed = (coords[0]+coords[1]+coords[2]+(coords[0]-1)+coords[1]+coords[2])
            random.seed(r_seed)
            loc_string = 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (coords[0]-1, coords[1], coords[2])
        elif i == 'west':
            r_seed = (coords[0]*coords[1]*coords[2]*coords[0]*(coords[1]+1)*coords[2])
            if r_seed == 0:
                r_seed = (coords[0]+coords[1]+coords[2]+coords[0]+(coords[1]+1)+coords[2])
            random.seed(r_seed)
            loc_string = 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (coords[0], coords[1]+1, coords[2])
        elif i == 'east':
            r_seed = (coords[0]*coords[1]*coords[2]*coords[0]*(coords[1]-1)*coords[2])
            if r_seed == 0:
                r_seed = (coords[0]+coords[1]+coords[2]+coords[0]+(coords[1]-1)+coords[2])
            random.seed(r_seed)
            loc_string = 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (coords[0], coords[1]-1, coords[2])
        elif i == 'up':
            if coords[2] < 0:
                r_seed = (coords[0]*coords[1]*coords[2]*coords[0]*coords[1]*(coords[2]+1))
                if r_seed == 0:
                    r_seed = (coords[0]+coords[1]+coords[2]+coords[0]+coords[1]+(coords[2]+1))
                random.seed(r_seed)
                loc_string = 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (coords[0], coords[1], coords[2]+1)
            else:
                t_add_exit = False
        elif i == 'down':
            r_seed = (coords[0]*coords[1]*coords[2]*coords[0]*coords[1]*(coords[2]-1))
            if r_seed == 0:
                r_seed = (coords[0]+coords[1]+coords[2]+coords[0]+coords[1]+(coords[2]-1))
            random.seed(r_seed)
            loc_string = 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (coords[0], coords[1], coords[2]-1)

        r = random.randint(0, 1)
        if r == 1 and t_add_exit == True:
            this_room.add_exit(i, loc_string)
    
    # Format: characteristic: % 
    light_levels = {'light': 62, 'dark': 38}
    temparture_levels = {'cool': 32, 'warm': 28, 'neutral': 40}
    water_levels = {'damp': 25, 'dry': 50, 'running': 15, 'lake': 10}

    hostility_levels = {'hostile':15, 'empty': 70, 'batty': 15}

    second_level_attrs = {'light': {'small opening': 10, 'smooth walls': 80,
                          'rough walls': 10}, 'dark':{'smooth walls': 50, 
                          'rough walls': 50}, 'cool':{'breeze': 50, 'NA': 50}, 'warm': {'warmpth': 70, 
                          'scalding floor': 29, 'pool of lava': 1}, 'neurtal': 
                          {'NA': 100}, 'neutral':{'NA':100}, 'damp': {'trickle of water': 10, 
                          'mossy': 40, 'damp air': 50}, 'dry': {'NA': 90, 'extremely dry': 10}, 
                          'running': {'waterfall': 30, 'underground stream': 70},
                          'lake': {'small underground lake': 50, 'large underground lake': 30, 
                          'small underground lake with waterfall': 5, 'large underground lake with waterfall': 15}}

    light_range_values = []
    for j in list(light_levels):
        for k in range(0, light_levels[j]):
            light_range_values.append(j)
    
    light_level = light_range_values[random.randint(0, 99)]
    
    temparture_range_values = []
    for l in list(temparture_levels):
        for m in range(0, temparture_levels[l]):
            temparture_range_values.append(l)
    
    temparture_level = temparture_range_values[random.randint(0, 99)]

    water_range_values = []
    for n in list(water_levels):
        for o in range(0, water_levels[n]):
            water_range_values.append(n)
    
    water_level = water_range_values[random.randint(0, 99)]

    hostility_range_values = []
    for p in list(hostility_levels):
        for q in range(0, hostility_levels[p]):
            hostility_range_values.append(p)
    
    hostility_level = hostility_range_values[random.randint(0, 99)]

    room_features = []
    for r in [light_level, temparture_level, water_level]:
        r_range_values = []
        for s in list(second_level_attrs[r]):
            for t in range(0, second_level_attrs[r][s]):
                r_range_values.append(s)
        feature = r_range_values[random.randint(0, 99)]
        room_features.append(feature)

    this_room.set_description('cavern','A test cavern. Coordinates: (%s, %s, %s). Features: %s, %s, %s' % (coords[0], coords[1], coords[2], room_features[0], room_features[1], room_features[2]))

    return this_room
