import time
import inspect

class DebugLog():
    """A simple class for printing or logging debug messages.
    
    Currently only supports printing and basic logging to a file."""
    def __init__(self, level=0):
        self.verbosity = int(level)  # current level of verbosity. 0 = no debug comments.     
        self.filter_str = '&&&'  # a default value unlikely to appear in any code or debug messages
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

    def set_filter_str(self, s):
        self.filter_str = s

    def debug(self, s = "default error msg", level = 1):
        """Print the string s if level is <= current verbosity level, or if s includes a 
        specified filter string. For example, if the filter string is set to 'Creature'
        then debug() will print any debug strings containing 'Creature'. """
        s = str(s)
        if level <= self.verbosity or self.filter_str in s:
            try:   #XXX temp fix
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
                s = "Error tracing stack, s = %s" % s
            print(s)
            if self.log:
                self.log.write("%s\n" % s)
        else:
            return

    def shut_down(self):
        """The function that closes down the DebugLog class and file."""
        self.log.close()
        self.log = None

dbg = DebugLog()