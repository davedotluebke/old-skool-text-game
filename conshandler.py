from logging import Handler

class ConsHandler(Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to one or more player consoles. Modified from StreamHandler in the 
    standard Python logging code, in Lib/logging/__init__.py
    """

    terminator = '\n'

    def __init__(self, cons=None, dbg_level="DEBUG"):
        """
        Initialize the handler.
        `cons` can be None or a single Console object
        """
        Handler.__init__(self, dbg_level)
        if cons:
            if hasattr(cons, "user"):  
                self.cons = [cons]
            else:
                raise  # specified `cons` is not a Console object!
        else:
            self.cons = []


    def flush(self):
        """
        Flushes the console(s).
        """
        self.acquire()
        try:
            for c in self.cons:
                if hasattr(c, "flush"):
                    c.flush()
        finally:
            self.release()

    def emit(self, record):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        The record is then written to the console with a trailing newline.  
        If exception information is present, it is formatted using
        traceback.print_exception and appended to the console.  
        """
        try:
            msg = self.format(record)
            for c in self.cons:
                c.write('```' + msg +'```' + self.terminator)
            self.flush()
        except RecursionError:  # See issue 36272 (python std library)
            raise
        except Exception:
            self.handleError(record)


    def __repr__(self):
        level = self.level
        name = self.cons.__repr__()  # getattr(self.cons, 'name', '')
        #  bpo-36015: name can be an int
        name = str(name)
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, level)

    def addConsole(self, c):
        """
        Add a user's console to the list of Consoles which receive 
        emits. If the console is already in the list, do nothing. 
        If the specified parameter is not a Console, raise an error.
        """
        if c not in self.cons:
            self.cons.append(c)

    def removeConsole(self, c):
        """Try to remove the given console from the list receiving emits"""
        try:
            self.cons.remove(c)
        except ValueError:
            pass  # not clear to what console or log we should print an error


