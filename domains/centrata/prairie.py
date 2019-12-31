# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

def load(param_list):
    path = param_list[0] # if paramaters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists
    
    prairie = room.Room('prairie', path)

    coords = (int(param_list[1]), int(param_list[2]))
    exit_probability = 0.9

    random.seed(coords)

    exit_directions = []
    
    if random.random() < exit_probability:
        prairie.add_exit('north', 'domains.centrata.prairie?%s&%s' % (coords[0], coords[1]-1))
        exit_directions.append('north')
    
    if random.random() < exit_probability:
        prairie.add_exit('south', 'domains.centrata.prairie?%s&%s' % (coords[0], coords[1]+1))
        exit_directions.append('south')
    
    if random.random() < exit_probability:
        prairie.add_exit('east', 'domains.centrata.prairie?%s&%s' % (coords[0]+1, coords[1]))
        exit_directions.append('east')
    
    if random.random() < exit_probability:
        prairie.add_exit('west', 'domains.centrata.prairie?%s&%s' % (coords[0]-1, coords[1]))
        exit_directions.append('west')
    
    prairie.set_description('prairie', 'This tallgrass prairie continues on in all directions') # TODO: Add more description based on exit_directions
    return prairie