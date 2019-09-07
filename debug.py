import time
import inspect

class DebugLog():
    """A simple class for printing or logging debug messages.
    
    Currently only supports printing and basic logging to a file."""
    def __init__(self, level=0):
        self.verbosity = {}          # map of current level of verbosity for player ids. 0 = no debug comments.     
        self.filter_strings = {}     # map of player ids to strings; print debug comments if any match
        self.ID_dict = {}
        self.set_logfile()

    def set_logfile(self, filename="test_log.txt"):
        self.filename = filename
        try: 
            self.log = open(self.filename, 'a')
            self.log.write("="*40 + "\n")
            self.log.write("New DebugLog session started " + time.asctime() + "\n")
        except FileNotFoundError:
            print("Could not find a file at %s. Creating a new one.\n" % (self.filename))
            self.log = open(self.filename, 'c')

    def set_filter_strings(self, s, ID):
        """Set a filter list s for the given player id."""
        self.filter_strings[ID] = s
    
    def set_verbosity(self, v, ID):
        """Set a verbosity v for the given player id."""
        self.verbosity[ID] = v

    def debug(self, s = "default error msg", level = 1):
        """Print the string s if level is <= current verbosity level, or if s includes 
        one of a list of specified filter strings. For example, if a filter string is 
        set to 'damage' then debug() prints any debug strings containing 'damage'.
        The debug string is prepended by a terse description of the call stack, so 
        filter strings will also catch class names e.g. 'Player' or 'Creature', and
        function names."""
        s = str(s)
        try:   
            stack = inspect.stack()     # returns a list of FrameInfo tuples
            class_name = stack[1].frame.f_locals["self"].__class__.__name__
            func_name = class_name + '.' + stack[1].function + ":" + str(stack[1].lineno)
            for f in stack[2:]:         
                try:
                    caller_class = f.frame.f_locals["self"].__class__
                    class_name = caller_class.__name__ + '.' if caller_class else ''
                except KeyError:
                    class_name = f.filename
                func_name = class_name + f.function + ":" + func_name
                if class_name == "Game.": break
            
            s = func_name + ": " + s
        except KeyError:
            s = "Error tracing stack, but debug message = %s" % s
        for player_id in list(self.verbosity):
            if level <= self.verbosity[player_id]:
                try:
                    self.ID_dict[player_id].cons.write(s)
                except Exception:
                    print("AN ERROR OCCURED!")
                    print(s)
        for player_id in list(self.filter_strings):
            found_match = any(filter_str in s for filter_str in self.filter_strings[player_id])
            if found_match:
                try:
                    self.ID_dict[player_id].cons.write(s)
                except Exception:
                    print("AN ERROR OCCURED!")
                    print(s)
        if self.log:
            self.log.write("%s\n" % s)

    def shut_down(self):
        """The function that closes down the DebugLog class and file."""
        self.log.close()
        self.log = None

dbg = DebugLog()
