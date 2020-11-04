# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

exit_probability = 0.91  # IMPORTANT must be same as below

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

# place orc camp in prairie, add to room_remaps
orc_camp_x = random.randint(int(MAX_X/2), MAX_X-1)
orc_camp_y = random.randint(int(MAX_Y/3), int((2*MAX_Y)/3))  #TODO: make sure there are exits from this room

room_remaps[f'{orc_camp_x},{orc_camp_y}'] = 'domains.centrata.orc_quest.orc_camp'
gametools.load_room('domains.centrata.orc_quest.orc_camp')  # do this so orcs begin wandering

# place footprints leading towards orc camp
footprint_routes = {}

def place_footprints(start_x, start_y):
    x = start_x
    y = start_y

    while x != MIN_X and x != MAX_X and y != MIN_Y and y != MAX_Y:

        possible_directions = []
        possible_direction_weights = []

        if connection_exists(x, y, 0, 1, exit_probability) and f'{x},{y+1}' not in room_remaps and f'{x},{y+1}' not in footprint_routes:
            possible_directions.append('north')
            if y < orc_camp_y:
                possible_direction_weights.append(0.1)
            else:
                possible_direction_weights.append(0.9)
        
        if connection_exists(x, y-1, 0, 1, exit_probability) and f'{x},{y-1}' not in room_remaps and f'{x},{y-1}' not in footprint_routes:
            possible_directions.append('south')
            if y > orc_camp_y:
                possible_direction_weights.append(0.1)
            else:
                possible_direction_weights.append(0.9)
        
        if connection_exists(x, y, 1, 0, exit_probability) and f'{x+1},{y}' not in room_remaps and f'{x+1},{y}' not in footprint_routes:
            possible_directions.append('east')
            if x < orc_camp_x:
                possible_direction_weights.append(0.1)
            else:
                possible_direction_weights.append(0.9)
        
        if connection_exists(x-1, y, 1, 0, exit_probability) and f'{x-1},{y}' not in room_remaps and f'{x-1},{y}' not in footprint_routes:
            possible_directions.append('west')
            if x > orc_camp_x:
                possible_direction_weights.append(0.1)
            else:
                possible_direction_weights.append(0.9)

        if not possible_directions:
            break

        direction = random.choices(possible_directions, possible_direction_weights)[0]

        if direction == 'north':
            y += 1
            footprint_routes[f'{x},{y}'] = 'south'
        
        if direction == 'south':
            y -= 1
            footprint_routes[f'{x},{y}'] = 'north'
        
        if direction == 'east':
            x += 1
            footprint_routes[f'{x},{y}'] = 'west'

        if direction == 'west':
            x -= 1
            footprint_routes[f'{x},{y}'] = 'east'
        

for i in range(0, 4):
    place_footprints(orc_camp_x, orc_camp_y)

def load(param_list):
    path = param_list[0] # if parameters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists

    coords = (int(param_list[1]), int(param_list[2]))
    x = coords[0]
    y = coords[1]
    
    if '%s,%s' % (x,y) in room_remaps:
        return gametools.load_room(room_remaps['%s,%s' % (x,y)])

    prairie = room.Room('prairie', path)

    no_exit_directions = []
    
    if connection_exists(x, y, 0, 1, exit_probability):
        prairie.add_exit('north', 'domains.centrata.orc_quest.prairie?%s&%s' % (coords[0], coords[1]+1))
    else:
        no_exit_directions.append('north')
    
    if connection_exists(x, y-1, 0, 1, exit_probability):
        prairie.add_exit('south', 'domains.centrata.orc_quest.prairie?%s&%s' % (coords[0], coords[1]-1))
    else:
        no_exit_directions.append('south')
    
    if connection_exists(x, y, 1, 0, exit_probability):
        prairie.add_exit('east', 'domains.centrata.orc_quest.prairie?%s&%s' % (coords[0]+1, coords[1]))
    else:
        no_exit_directions.append('east')
    
    if connection_exists(x-1, y, 1, 0, exit_probability):
        prairie.add_exit('west', 'domains.centrata.orc_quest.prairie?%s&%s' % (coords[0]-1, coords[1]))
    else:
        no_exit_directions.append('west')
    
    random.seed(coords)

    prairie_details = [('a flock of birds',
    'This flock of birds is perched in the corner of the field.',
    ['birds', 'flock'], ['perched']),
    ('a small tree',
    'This small tree has %s.' % random.choice('a jagged bend in the middle of its trunk', 
    'sparse and withered branches', 'a small patch of shade below it'),
    ['tree'], ['small']),
    ('a field of bluets',
    'This field of bluets poke up from the prairie like raindrops.',
    ['field', 'bluet', 'bluets'], ['field', 'bluet']),
    ('a small pond',
    'This small pond is %s.' % random.choice('muddy and stagnant', 'clear and empty',
    ['pond'], ['muddy', 'stagnant', 'clear', 'empty']),
    ('a big bush',
    'This unusually large bush stands out from the prairie around it. It is dark green and appears to be very sharp.',
    ['bush'], ['large', 'green', 'dark', 'sharp'])]
    blocking_details = [('a group of trees',
    'This large and thick group of trees stands to the %s, making passage all but impossible.',
    ['trees', 'tree'], ['large', 'thick']),
    ('a big herd of bison', 'This big herd of bison stands to the %s.',
    ['bison', 'herd'], ['big', 'herd'])]

    num_non_blocking_details = random.randint(0, 2)
    num_blocking_details = len(no_exit_directions)

    notable_items = []
    if f'{x},{y}' in footprint_routes:
        notable_items.append('footprints coming from the %s' % footprint_routes[f'{x},{y}'])

    total_num_details = num_non_blocking_details + num_blocking_details + len(notable_items)
    notable_string = '%s, '*(total_num_details - 1) + 'and %s.'

    for i in range(0, num_blocking_details):
        blocking_item = random.choice(blocking_details)
        notable_items.append(blocking_item[0] + ' to the ' + no_exit_directions[i])

        blocking_scenery_item = scenery.Scenery(blocking_item[2][0], blocking_item[0], blocking_item[1] % no_exit_directions[i], unlisted=True)
        blocking_scenery_item.add_names(*blocking_item[2])
        blocking_scenery_item.add_adjectives(*blocking_item[3])
        blocking_scenery_item.add_adjectives(no_exit_directions[i])
        blocking_scenery_item.move_to(prairie, True)

    for i in range(0, num_non_blocking_details):
        prairie_item = random.choice(prairie_details)
        notable_items.append(prairie_item[0])

        prairie_scenery_item = scenery.Scenery(prairie_item[2][0], prairie_item[0], prairie_item[1], unlisted=True)
        prairie_scenery_item.add_names(*prairie_item[2])
        prairie_scenery_item.add_adjectives(*prairie_item[3])
        prairie_scenery_item.move_to(prairie, True)

    random.shuffle(notable_items)

    if len(notable_items):  # TODO: "Scenery" objects for notable_items
        notable_string = notable_string % tuple(notable_items)
        prairie.set_description('prairie', 'You find yourself in a tallgrass prairie. You notice %s' % notable_string)
    else:
        prairie.set_description('prairie', 'You find yourself in a tallgrass prairie that stetches on in all directions.')
    return prairie
