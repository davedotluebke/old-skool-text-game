from logging import Handler
import console


class ConsHandler(Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to the console of a player. Modified from StreamHandler in the standard
    Python logging code, in Lib/logging/__init__.py
    """

    terminator = '\n'

    def __init__(self, cons=None, dbg_level="DEBUG"):
        """
        Initialize the handler.
        If cons is not specified, raise an exception
        """
        Handler.__init__(self, dbg_level)
        if cons is None:
            raise 
        self.cons = cons

    def flush(self):
        """
        Flushes the console.
        """
        self.acquire()
        try:
            if self.cons and hasattr(self.cons, "flush"):
                self.cons.flush()
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
            cons = self.cons
            cons.write('```' + msg +'```' + self.terminator)
            self.flush()
        except RecursionError:  # See issue 36272 (python std library)
            raise
        except Exception:
            self.handleError(record)

    

    def __repr__(self):
        level = self.level
        name = getattr(self.cons, 'name', '')
        #  bpo-36015: name can be an int
        name = str(name)
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)
