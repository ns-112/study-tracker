class timeline:
    
    def __init__(self):
        self.events = {}
        pass
    def add_event(self, time, event):
        self.events[event] = time