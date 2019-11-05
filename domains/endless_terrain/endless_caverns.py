# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import numpy as np

import gametools
import scenery
import room
import random
from debug import dbg

def connection_exists(x, y, z, delta_x, delta_y, delta_z, threshold):
    """Return a true or false indicating whether a grid cell at 
    (x, y, z) has a connection in direction (delta_x, delta_y, delta_z), 
    where delta_x, delta_y, and delta_z are 0 or 1. For consistency, always 
    check for a connection FROM the room with the most negative index TO the
    room with most positive index.  E.g. to see if room (3, 4,-2) has a 
    connection to the north, check (3,4,-2,(0,1,0)). For a connection to the
    south, check (3,3,-2, (0,1,0)). Uses a random number seeded on combination 
    of bits from the inputs and compares it to the provided threshold."""
    x_bits = (x & 0xff) << 19
    y_bits = (y & 0xff) << 11
    z_bits = (z & 0xff) << 3
    delta_x_bits = (delta_x & 0x01) << 2
    delta_y_bits = (delta_y & 0x01) << 1
    delta_z_bits = (delta_z & 0x01)
    all_bits = x_bits | y_bits | z_bits | delta_x_bits | delta_y_bits | delta_z_bits
    random.seed(all_bits)
    num = random.random()
    #dbg.debug("Coordinates: %s, %s, %s. Direction: %s, %s, %s. Seed: %s. Num: %s" % (x, y, z, delta_x, delta_y, delta_z, all_bits, num))
    return num < threshold

masks = {'north':0x01, 'south':0x02, 'east':0x04, 'west':0x08, 'up':0x10, 'down':0x20}

def depth_first_search(t, start_x=-30,start_y=-30,start_z=-2,end_x=30,end_y=30,end_z=2,start_label=1):
    directions = {'north': (0,  1,  0 ), 
                  'south': (0, -1,  0 ),
                  'east':  (1,  0,  0 ),
                  'west':  (-1, 0,  0 ),
                  'up':    (0,  0,  1 ), 
                  'down':  (0,  0, -1 )}
    visited = np.zeros(t.shape, dtype=np.int32)
    
    def visit_point(x, y, z, label):  
        """Recursively visit a point P=(x,y,z) and all connections of P.
        Assign label to P if it has not already been labeled.
        Return the number of points had their label changed"""
        if not ((start_x < x < end_x) and (start_y < y < end_y) and (start_z < z < end_z)):
            return 0
        if visited[x, y, z] != 0:
            return 0
        visited[x, y, z] = label
        changed = 1
        for e in masks:
            if t[x, y, z] & masks[e]:
                changed += visit_point(x+directions[e][0], y+directions[e][1], z+directions[e][2], label)
        return changed
    
    for a in range(start_x, end_x):
        for b in range(start_y, end_y):
            for c in range(start_z, end_z):
                if visit_point(a, b, c, start_label): 
                    start_label += 1  # increment the label if we labeled one or more points
    
    return visited

def test_grid(cons=None, exit_probability = 0.25):
    table = np.zeros((60,60,4), dtype=np.int32)
    for i in range(-30, 30):
        for j in range(-30, 30):
            for k in range(-2, 2):
                possible_directions = []
                directions_mask = 0x00

                x = j+30
                y = i+30
                z = k+2

                for direction, d_xyz in [ ('north', (0,  1,  0 )), 
                                        ('south', (0, -1,  0 )), 
                                        ('east',  (1,  0,  0 )),
                                        ('west',  (-1, 0,  0 )), 
                                        ('up',    (0,  0,  1 )), 
                                        ('down',  (0,  0, -1 )) ]:
                    # see if a connection exists between this room and the room to the east (x+1), 
                    # west (x-1), north (y+1), etc.  
                    check_x = x if d_xyz[0] >= 0 else x-1
                    check_y = y if d_xyz[1] >= 0 else y-1
                    check_z = z if d_xyz[2] >= 0 else z-1

                    check_dx = 1 if d_xyz[0] != 0 else 0
                    check_dy = 1 if d_xyz[1] != 0 else 0
                    check_dz = 1 if d_xyz[2] != 0 else 0

                    if connection_exists(check_x, check_y, check_z, check_dx, check_dy, check_dz, exit_probability):
                        possible_directions.append(direction)
                        directions_mask |= masks[direction]
            
                table[x,y,z] = directions_mask
    
    centers = depth_first_search(table, -30, -30, -2, 30, 30, 2, 1)
    
    # create an ascii art depiction of the cavern map, with each room represented by a 3x3 grid of characters
    # note north is direction of increasing y, i.e. first row in table is the southmost row on map. 
    map_str = ""
    for i in range(0, table.shape[0]):
        # make 3 strings per row, to be printed as consecutive lines
        line1 = ""
        line2 = ""
        line3 = ""
        for j in range(0, table.shape[1]):
            # make 3 characters in each line for each element
            mask = table[j,i,2]
            line1 += " | " if mask & masks['north'] else "   "
            line2 += "-" if mask & masks['west'] else " "
            if mask & (masks['north'] | masks['south'] | masks['east'] | masks['west']) :  
                # ignore up and down for now, draw + if room has a NSEW exit or ' ' if not
                line2 += chr(47+(centers[j,i,0] % 74))
            else:
                line2 += " "
            line2 += "-" if mask & masks['east'] else " "
            line3 += " | " if mask & masks['south'] else "   "
        # i=0 is the bottom (southmost) row of map, so build map from bottom up
        # therefore these three lines go on top of the map so far (i.e. before the current map string)
        map_str = line1 + "\n" + line2 + '\n' + line3 + '\n' + map_str
    print(map_str)
    if cons:
        cons.write(map_str.replace(' ','&nbsp'))


        
def load(param_list):
    path = param_list[0] # if paramaters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists
    
    coords = [int(param_list[1]), int(param_list[2]), int(param_list[3])]

    this_room = room.Room('cave', path)

    exit_probability = 0.25

    x = coords[0]
    y = coords[1]
    z = coords[2]

    for direction, d_xyz in [('north', (0,  1,  0 )), 
                             ('south', (0, -1,  0 )), 
                             ('east',  (1,  0,  0 )),
                             ('west',  (-1, 0,  0 )), 
                             ('up',    (0,  0,  1 )), 
                             ('down',  (0,  0, -1 ))]:
        # see if a connection exists between this room and the room to the east (x+1), 
        # west (x-1), north (y+1), etc.  
        check_x = x if d_xyz[0] >= 0 else x-1
        check_y = y if d_xyz[1] >= 0 else y-1
        check_z = z if d_xyz[2] >= 0 else z-1

        check_dx = 1 if d_xyz[0] != 0 else 0
        check_dy = 1 if d_xyz[1] != 0 else 0
        check_dz = 1 if d_xyz[2] != 0 else 0

        if connection_exists(check_x, check_y, check_z, check_dx, check_dy, check_dz, exit_probability):
            this_room.add_exit(direction, 'domains.endless_terrain.endless_caverns?%s&%s&%s' % (x+d_xyz[0], y+d_xyz[1], z+d_xyz[2]))
    
    # Format: characteristic: % 
    light_levels = {'light': 62, 'dark': 38}
    temperature_levels = {'cool': 32, 'warm': 28, 'neutral': 40}
    water_levels = {'damp': 25, 'dry': 50, 'running': 15, 'lake': 10}

    hostility_levels = {'hostile':15, 'empty': 70, 'batty': 15}

    second_level_attrs = {'light': {'small opening': 10, 'smooth walls': 80, 'rough walls': 10}, 
                          'dark': {'smooth walls': 50, 'rough walls': 50}, 
                          'cool': {'breeze': 50, 'NA': 50}, 
                          'warm': {'warmth': 70, 'scalding floor': 29, 'pool of lava': 1}, 
                          'neutral': {'NA': 100}, 
                          'neutral':{'NA':100}, 
                          'damp': {'trickle of water': 10, 'mossy': 40, 'damp air': 50}, 
                          'dry': {'NA': 90, 'extremely dry': 10}, 
                          'running': {'waterfall': 30, 'underground stream': 70},
                          'lake': {'small underground lake': 50, 'large underground lake': 30, 'small underground lake with waterfall': 5, 'large underground lake with waterfall': 15}}

    light_range_values = []
    for j in list(light_levels):
        for k in range(0, light_levels[j]):
            light_range_values.append(j)
    
    light_level = light_range_values[random.randint(0, 99)]
    
    temperature_range_values = []
    for l in list(temperature_levels):
        for m in range(0, temperature_levels[l]):
            temperature_range_values.append(l)
    
    temperature_level = temperature_range_values[random.randint(0, 99)]

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
    for r in [light_level, temperature_level, water_level]:
        r_range_values = []
        for s in list(second_level_attrs[r]):
            for t in range(0, second_level_attrs[r][s]):
                r_range_values.append(s)
        feature = r_range_values[random.randint(0, 99)]
        room_features.append(feature)
    
    this_room.set_description('cavern','A test cavern. Coordinates: (%s, %s, %s). Features: %s, %s, %s' % (coords[0], coords[1], coords[2], room_features[0], room_features[1], room_features[2]))

    return this_room
