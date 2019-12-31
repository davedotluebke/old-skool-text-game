import os
import importlib
from debug import dbg
from walking_os import findAllPythonFiles

# the top-level or 'root' directory of the game. Note, assumes this file (gametools.py) is at the root
gameroot = os.path.dirname(__file__) 

PLAYER_DIR = os.path.join(gameroot, "saved_players")
PLAYER_BACKUP_DIR = os.path.join(gameroot, "backup_saved_players")
NEW_PLAYER_START_LOC = 'domains.character_creation.start_loc'
DEFAULT_START_LOC = 'domains.school.school.great_hall'

class PlayerSaveError(Exception):
    pass

class PlayerLoadError(Exception):
    pass

class IncorrectPasswordError(Exception):
    pass

def validate_func(modpath, func):
    try:
        mod = importlib.import_module(modpath)
        if hasattr(mod, func):
            return True
        else:
            return False
    except ImportError:
        dbg.debug("Error checking load on module %s: no module with path" % modpath)
        return False

def clone(obj_module, params=None):
    '''Load specified module, call its clone() method, and return the resulting object.
    The object's module should be specified in python package format relative to the
    root of the game source tree, e.g. "domains.school.sword" refers to the python module
        ${gameroot}/domains/school/sword.py.'''
    try: 
        mod = importlib.import_module(obj_module)
        if params:
            obj = mod.clone(params)
        else:
            obj = mod.clone()
        obj.mod = mod
    except ImportError:
        dbg.debug("Error importing module %s" % obj_module)
        return None
    except AttributeError:
        dbg.debug("Error cloning from module %s: no clone() method" % obj_module)
        return None
    if obj == None:
        dbg.debug("Error cloning from module %s: clone() return None" % obj_module)
    return obj

def deconstructObjectPath(path_str):
    path, sep, parameters = path_str.partition('?')
    if parameters:
        return path, [path_str]+parameters.split('&')
    return path, None

def load_room(modpath, report_import_error=True):
    """Attempt to load a room from its modpath (e.g. 'domains.school.testroom'). 
    If an ImportEerror occurs, will attempt to create a room if given paramaters.
    Returns a reference to the room, or None if the given modpath could not be loaded."""
    try: 
        roomString, params = deconstructObjectPath(modpath)
        mod = importlib.import_module(roomString)
        if params:
            room = mod.load(params)
        else:
            room = mod.load()
        room.mod = mod # store the module to allow for reloading later
        room.params = params
    except ImportError:
        if report_import_error:
            dbg.debug("Error importing room module %s" % modpath)
        return None
    except AttributeError:
        dbg.debug("Error loading from room module %s: no load() method" % modpath)
        return None
    if room == None:
        dbg.debug("Error loading from room module %s:load() returned None" % modpath)
    return room
    
def findGamePath(filepath):
    gamePath = os.path.relpath(filepath, gameroot).replace("\\", ".").replace("/", ".")
    (head, sep, tail) = gamePath.partition(".py")
    gamePath = head
    return gamePath

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]

def request_all_inputs(player, dest):
    Thing.ID_dict[player].cons.request_input(dest)
