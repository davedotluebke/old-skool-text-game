from logging import Handler


class AccessPointHandler(Handler):
    """
    A handler class which writes logging records, appropriately formatted,
    to the console of a player through the access point. Modified from 
    StreamHandler in the standard Python logging code, in Lib/logging/__init__.py
    """

    terminator = '\n'

    def __init__(self, access_point=None, dbg_level="DEBUG"):
        """
        Initialize the handler.
        If access_point is not specified, raise an exception
        """
        Handler.__init__(self, dbg_level)
        if access_point is None:
            raise 
        self.access_point = access_point

    def flush(self):
        """
        Flushes the access_point.
        """
        self.acquire()
        try:
            if self.access_point.transport and hasattr(self.access_point.transport, "flush"):
                self.access_point.flush()
        finally:
            self.release()

    def emit(self, record):
        """
        Emit a record.
        If a formatter is specified, it is used to format the record.
        The record is then written to the access point with a trailing newline.  
        If exception information is present, it is formatted using
        traceback.print_exception and appended to the access point.  
        """
        try:
            msg = self.format(record)
            access_point = self.access_point
            access_point.send_message('```' + msg +'```' + self.terminator)
            self.flush()
        except RecursionError:  # See issue 36272 (python std library)
            raise
        except Exception:
            self.handleError(record)

    

    def __repr__(self):
        level = self.level
        name = getattr(self.access_point, 'name', '')
        #  bpo-36015: name can be an int
        name = str(name)
        if name:
            name += ' '
        return '<%s %s(%s)>' % (self.__class__.__name__, name, level)
