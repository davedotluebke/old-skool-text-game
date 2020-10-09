# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

room_remaps = {'-1,-1':'domains.centrata.fields.road_three',
               '-1,0':'domains.centrata.fields.road_four',
               '-1,1':'domains.centrata.fields.road_five',
               '-1,2':'domains.centrata.fields.road_six',
               '-1,3':'domains.centrata.fields.road_seven',
               '-1,4':'domains.centrata.fields.road_eight',
               '0,-2':'domains.centrata.fields.road_two',
               '0,2':'domains.centrata.fields.questentry',
               '1,-3':'domains.centrata.fields.road_one',
               '0,4':'domains.centrata.fields.small_wooded_patch',
               '1,5':'domains.centrata.fields.behind_blacksmith_shop',
               '1,6':'domains.centrata.fields.behind_tailors_shop'}

MIN_X = -1 # dictated by coordinates in room_remaps
MAX_X = 9
MIN_Y = -3 # dictates by coordinates in room_remaps
MAX_Y = 7

def connection_exists(x, y, delta_x, delta_y, threshold):
    """Return a true or false indicating whether a grid cell at 
    (x, y) has a connection in direction (delta_x, delta_y), 
    where delta_x and delta_y are 0 or 1. For consistency, always 
    check for a connection FROM the room with the most negative index TO the
    room with most positive index.  E.g. to see if room (3, 4) has a 
    connection to the north, check (3,4,(0,1)). For a connection to the
    south, check (3,3, (0,1)). Uses a random number seeded on combination 
    of bits from the inputs and compares it to the provided threshold."""

    if x < MIN_X:
        return False
    if x+1 > MAX_X:
        return False
    if y < MIN_Y:
        return False
    if y+1 > MAX_Y:
        return False
    x_bits = (x & 0xff) << 10
    y_bits = (y & 0xff) << 2
    delta_x_bits = (delta_x & 0x01) << 1
    delta_y_bits = (delta_y & 0x01)
    all_bits = x_bits | y_bits | delta_x_bits | delta_y_bits
    random.seed(all_bits)
    num = random.random()
    return num < threshold

def load(param_list):
    path = param_list[0] # if parameters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists

    coords = (int(param_list[1]), int(param_list[2]))
    x = coords[0]
    y = coords[1]
    exit_probability = 0.91
    
    if '%s,%s' % (x,y) in room_remaps:
        return gametools.load_room(room_remaps['%s,%s' % (x,y)])

    prairie = room.Room('prairie', path)

    no_exit_directions = []
    
    if connection_exists(x, y, 0, 1, exit_probability):
        prairie.add_exit('north', 'domains.centrata.prairie?%s&%s' % (coords[0], coords[1]+1))
    else:
        no_exit_directions.append('north')
    
    if connection_exists(x, y-1, 0, 1, exit_probability):
        prairie.add_exit('south', 'domains.centrata.prairie?%s&%s' % (coords[0], coords[1]-1))
    else:
        no_exit_directions.append('south')
    
    if connection_exists(x, y, 1, 0, exit_probability):
        prairie.add_exit('east', 'domains.centrata.prairie?%s&%s' % (coords[0]+1, coords[1]))
    else:
        no_exit_directions.append('east')
    
    if connection_exists(x-1, y, 1, 0, exit_probability):
        prairie.add_exit('west', 'domains.centrata.prairie?%s&%s' % (coords[0]-1, coords[1]))
    else:
        no_exit_directions.append('west')
    
    random.seed(coords)

    prairie_details = ['a flock of birds', 'a small tree', 'a field of bluets', 'a small pond', 'a big bush']
    blocking_details = ['a group of trees', 'a big herd of bison']

    num_non_blocking_details = random.randint(0, 2)
    num_blocking_details = len(no_exit_directions)
    total_num_details = num_non_blocking_details + num_blocking_details
    notable_string = '%s, '*(total_num_details - 1) + 'and %s.'

    notable_items = []
    for i in range(0, num_blocking_details):
        notable_items.append(random.choice(blocking_details) + ' to the ' + no_exit_directions[i])
    for i in range(0, num_non_blocking_details):
        notable_items.append(random.choice(prairie_details))
    random.shuffle(notable_items)

    if len(notable_items): # TODO: "Scenery" objects for notable_items
        notable_string = notable_string % tuple(notable_items)
        prairie.set_description('prairie', 'You find yourself in a tallgrass prairie. You notice %s' % notable_string)
    else:
        prairie.set_description('prairie', 'You find yourself in a tallgrass prairie that stetches on in all directions.')
    return prairie
