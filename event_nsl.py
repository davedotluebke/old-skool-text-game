import sys

class Event:
    def __init__(self, timestamp, callback, payload):
        self.timestamp = timestamp
        self.callback = callback
        self.payload = payload

    def activate(self):
        self.callback(self.payload)

class EventQueue:
    def __init__(self):
        sentinel = Event(sys.maxsize, None, None)     # an event at the end of time
        self.Q = [sentinel]
    
    # TODO: make this more efficient. Right now it re-sorts every time
    def schedule(self, timestamp, callback, payload=None):
        ev = Event(timestamp, callback, payload)
        index = 0
        for w in self.Q:
            if w.timestamp < ev.timestamp:
                index += 1
        self.Q.insert(index, ev)

    def check_for_event(self, time):
        """Return a (possibly empty) list of events scheduled on or before the given time"""
        ev_list = []
        while self.Q[0].timestamp <= time:  # sentinel avoids an IndexError
            ev_list.append(self.Q[0])
            del self.Q[0]
        return ev_list