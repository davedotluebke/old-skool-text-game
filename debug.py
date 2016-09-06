import time

class DebugLog():
    """A simple class for printing or logging debug messages.
    
    Currently only supports printing and basic logging to a file."""
    def __init__(self, level=0):
        print("DebugLog __init__() called! This should only happen once.")
        self.verbosity = int(level)  # current level of verbosity. 0 = no debug comments.  
        self.filename = input("Please enter the filename of the main game's location: ")
        try: 
            self.log = open(self.filename, 'a')
            self.log.write("="*40 + "\n")
            self.log.write("New DebugLog session started " + time.asctime())
        except FileNotFoundError:
            print("could not find a file at %s. Creating a new one." % (self.filename))
            self.log = open(self.filename, 'c')

    def debug(self, s = "default error msg", level = 1):
        """Print the string s if level is <= current verbosity level."""
        if level <= self.verbosity:
            print(s)
        self.log.write(s + "\n")

    def shut_down(self):
        """The function that closes down the DebugLog class and file."""
        self.log.close()



dbg = DebugLog()