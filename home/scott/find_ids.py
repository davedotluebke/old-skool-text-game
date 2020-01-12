import thing

def find_id(s):
    matches = []
    for i in thing.Thing.ID_dict:
        if i.startswith(s):
            matches.append(i)
    return matches
