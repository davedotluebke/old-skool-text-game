# Room Factory: This module will create multiple rooms, depending on what paramaters are called in the load function
import gametools
import scenery
import room
import random

coord_dict = {
    '0,0': 'domains.archipel.monument'
}

def load(param_list):
    path = param_list[0] # if parameters are given, the first one is always the entire string, including parameters
    exists = room.check_loaded(path)
    if exists: return exists

    x = int(param_list[1])
    y = int(param_list[2])

    if f'{x},{y}' in coord_dict.keys():
        return gametools.load_room(coord_dict[f'{x}, {y}'])
    
    ocean = room.Room('ocean', path)
    ocean.set_description('open ocean', 'This is the open ocean. The waves are fairly calm today.')
    ocean.add_exit('north', f'domains.archipel.open_ocean?{x}&{y+1}')
    ocean.add_exit('south', f'domains.archipel.open_ocean?{x}&{y-1}')
    ocean.add_exit('east',  f'domains.archipel.open_ocean?{x+1}&{y}')
    ocean.add_exit('west',  f'domains.archipel.open_ocean?{x-1}&{y}')

    return ocean
