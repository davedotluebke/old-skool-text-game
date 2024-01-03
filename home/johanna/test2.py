import thing
import gametools

# This is an example file for testing. Current date: 3 January 2024, #16

def find_id(s):
    matches = []
    for i in thing.Thing.ID_dict:
        if i.startswith(s):
            matches.append(i)
    return matches
