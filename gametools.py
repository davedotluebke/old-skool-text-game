import os
import platform
import importlib
import logging
from walking_os import findAllPythonFiles

#
# GLOBAL GAME ATTRIBUTES
#   Convention: all directories and files are relative to the game file system,
#   which is rooted in the real file system at "gameroot". It is the responsibility
#   of the code using these globals to prepend gameroot if needed at the point of use.
#
gameroot = os.path.dirname(__file__)  # the top-level or 'root' directory of the game. Note, assumes this file (gametools.py) is at the root

GAME_LOG = "/game_log.txt"
PLAYER_ROLES_FILE = "/player_roles.json"
PLAYER_DIR = "/saved_players"
PLAYER_BACKUP_DIR = "/backup_saved_players"
DOMAIN_DIR = "/domains/"
HOME_DIR = "/home/"

NEW_PLAYER_START_LOC = "domains.character_creation.start_loc"
DEFAULT_START_LOC = "domains.school.school.great_hall"

console_error_codes = {0: {"name": 'success', "description": 'The action succeeded.'},
400: {"name": 'Missing parameter', "description": 'The console has not sent a parameter required for operation, e.g. no `type` set ot no `message` on a parse request.'},
401: {"name": 'JSON error', "description": 'JSON is unreadable or encoded wrong'},
406: {"name": 'User definition error', "description": '`AcessPoint.user` is set when it shouldn\'t be or vice versa'},
500: {"name": 'Generic error', "description": 'used if no other error type fits. Better to create a new error type.'},
501: {"name": 'Python error', "description": 'Happens when an Python error has occurred in the server that causes the request to be unfulfillable. Traceback should be in `response.message`.'}}

#
# CUSTOM EXCEPTIONS
#
class PlayerSaveError(Exception):
    pass

class PlayerLoadError(Exception):
    pass

class IncorrectPasswordError(Exception):
    pass

class BadSpellInfoError(AttributeError):
    pass

#
# UTILITY FUNCTIONS
# 
def normGameDir(gamedir:str):
    """Collapse redundant separators and up-level references so that
    A//B, A/B/, A/./B and A/foo/../B all become A/B. Uses os.path.normpath()
    but (on Windows) then replaces backslashes with forward slashes, since 
    game directory paths use forward slashes as a separator."""
    if platform.system() == 'Windows':
        return os.path.normpath(gamedir).replace('\\','/')
    else:
        return os.path.normpath(gamedir)

def expandGameDir(gamedir:str, player:str=None):
    """Expand leading tilde character: if first character is '~',
    ~wizard becomes /home/wizard and ~ becomes /home/{player}"""
    root, sep, rest = gamedir.partition('/')
    if root and root[0] == '~':
        if root == '~':
            if player:
                return '/home/'+player+'/'+rest
            else:
                return '/home/{ERROR NO PLAYER SPECIFIED}/'+rest
        else:
            return '/home/'+root[1:]+'/'+rest
    else:
        return gamedir
        
def realDir(*gamedir, player=None):
    """Convert path(s) rooted in the game filesystem to the real filesystem.
    This is done by expanding the leading ~ shortcut, if any, in the first
    argument to a home directory; then stripping any leading slashes; then 
    joining this path and any others; then prepending the result with the 
    `gameroot` directory path (which is rooted in the real filesystem); then
    finally converting the result to a "normalized path", e.g. removing
    duplicate slashes and converting to backslashes if on Windows."""
    realdir = os.path.join(expandGameDir(gamedir[0], player), *gamedir[1:]).lstrip('/')
    return os.path.normpath(os.path.join(gameroot, realdir))

def findGamePath(filepath):
    """ Change an OS filename path (separated by forward or backward slashes) to a 
    python-style module path separated by periods."""
    gamePath = os.path.relpath(filepath, gameroot).replace("\\", ".").replace("/", ".")
    (head, sep, tail) = gamePath.partition(".py")
    gamePath = head
    return gamePath

def deconstructObjectPath(path_str):
    """The game refers to object paths using python-style module paths separated by 
    periods, but wizards can add parameters to be passed to the objects by adding 
    a ? character after the object path and then separating multiple parameters by 
    the & character. See domains.centrata.prairie.py for an example of this usage."""
    path, sep, parameters = path_str.partition('?')
    if parameters:
        return path, [path_str]+parameters.split('&')
    return path, None

def check_player_exists(p):
    """Return whether a given player exists, i.e. has a save file."""
    filename = realDir(PLAYER_DIR, p) + '.OADplayer'
    try:
        f = open(filename, 'r+b')
        f.close()  # success, player exists, so close file for now
        return True
    except FileNotFoundError: 
        return False
        
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

#
# LOGGING 
#
game_log_handler = logging.FileHandler(realDir(GAME_LOG))
game_log_handler.setLevel(logging.WARNING)
game_log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
game_log_handler.setFormatter(game_log_formatter)

def get_game_logger(obj, printing=False):
    """Returns the logger associated with object `obj`, creating if needed. All
       objects log messages to the default logfile via game_log_handler; if 
       <printing> is set to True, messages are also printed to stderr."""
    if isinstance(obj, str):
        logname = obj
    else:
        if obj.path:
            # name the log for this object by its path + id, unless id already == path (Rooms)
            logname = obj.path + "" if obj.id==obj.path else ":"+obj.id
        else:
            logname = obj.id
    logger = logging.getLogger(logname)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(game_log_handler)
    if printing:
        logger.addHandler(logging.StreamHandler())
    return logger

#
# OBJECT CREATION/LOADING FUNCTIONS
#
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
        get_game_logger("_gametools").error("Error importing module %s" % obj_module)
        return None
    except AttributeError:
        get_game_logger("_gametools").error("Error cloning from module %s: no clone() method" % obj_module)
        return None
    if obj == None:
        get_game_logger("_gametools").error("Error cloning from module %s: clone() return None" % obj_module)
    return obj

def load_room(modpath, report_import_error=True):
    """Attempt to load a room from its modpath (e.g. 'domains.school.testroom'). 
    If an ImportEerror occurs, will attempt to create a room if given parameters.
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
            get_game_logger("_gametools").error("Error importing room module %s" % modpath)
        return None
    except AttributeError:
        get_game_logger("_gametools").error("Error loading from room module %s: no load() method" % modpath)
        return None
    if room == None:
        get_game_logger("_gametools").error("Error loading from room module %s:load() returned None" % modpath)
    return room
