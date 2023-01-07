import thing
import gametools

# This is an example file for testing. Current date: 1 March 2020, #11
def find_id(s):
    matches = []
    for i in thing.Thing.ID_dict:
        if i.startswith(s):
            matches.append(i)
    return matches
