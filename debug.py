class DebugLog():
    """A simple class for printing or logging debug messages.
    
    Currently only supports printing; later will support logging to a file."""
    def __init__(self, level=0):
        print("DebugLog __init__() called! This should only happen once.")
        self.verbosity = int(level)  # current level of verbosity. 0 = no debug comments.  

    def debug(self, s = "default error msg", level = 1):
        """Print the string s if level is <= current verbosity level."""
        if level <= self.verbosity:
            print(s)
    

dbg = DebugLog()