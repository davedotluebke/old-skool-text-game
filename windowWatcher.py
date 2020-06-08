import creature

class WindowWatcher(creature.NPC):
    def __init__(self, file):
        super().__init__('windowWatcher', file)
        self.invisible = True
        self.unlisted = True
    
    def heartbeat(self):
        self.health = 1000000000
    
    def perceive(self, message):
        super().perceive(message)
        self.window_obj.get_window_message(message)

def clone():
    w = WindowWatcher(__file__)
    return w