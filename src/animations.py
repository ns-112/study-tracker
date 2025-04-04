
class animation:
    def __init__(self, object, x = 0, y = 0):
        self.keyframes = []
        self.index = 0
        self.origin = (x, y)
        self.object = object


    def animate(self, deltatime):
        key = self.keyframes[self.index]
        self.object = (self.lerp(key.x1, key.x2, key.lerpval), self.lerp(key.y1, key.y2, key.lerpval))
        pass
    
    def lerp(start, end, t):
        return (1 - t) * start + t * end
    
    
    
    
    
class keyframe(animation):
    def __init__(self, time, x, y, ease = "linear"):
        if len(super().keyframes) > 0:
            self.x1 = super().keyframes[-1].x2
            self.y1 = super().keyframes[-1].y2
        else:
            self.x1 = super().origin[0]
            self.x2 = super().origin[1]
        self.x2 = x
        self.y2 = y
        self.time = time
        self.easing = ease
        self.lerpval = 0
        for i in super().keyframes:
            if self.time == i:
                self.time = i + 0.001
                break
        super().keyframes.append(self)


        



