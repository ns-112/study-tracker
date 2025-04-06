import pyautogui
import numpy as np
import pygame

#fix this to be dynamic
WIDTH = 1280
HEIGHT = 720
BASE_POS = (WIDTH // 2, HEIGHT // 2)
print(BASE_POS)

'''
main object class that can contain
animation tracks which include
keyframes
'''
class object:
    def __init__(self, object, screen, origin = (0, 0)):
        self.position = []
        self.scale = []    
        #todo   
        self.rotation = []
        #todo maybe
        self.skew = []

        self.surface = screen
        self.object = object
        self.object_copy = object
        self.object_rect = pygame.Rect(BASE_POS[0] + origin[0], BASE_POS[1] + (-origin[1]), object.get_rect()[2], object.get_rect()[3])

    '''
    create and append new animation track
    '''
    def addAnimationTrack(self, type, keyframes, start = (0, 0), loop = False, argument1 = False, argument2 = False, argument3 = False):
        anim = animation(type, keyframes, origin = start, does_loop = loop, arg1 = argument1, arg2 = argument2, arg3 = argument3)
        self.addAnimationFromClass(anim)

    '''
    add animation system to main object's list of references.
    this allows the user to add multiple animation tracks of the same type, hopefully
    allowing for some interesting animations
    '''
    def addAnimationFromClass(self, animation):
        if (animation.anim_type == "p"):
            self.position.append(animation)
        if (animation.anim_type == "s"):
            self.scale.append(animation)
        if (animation.anim_type == "r"):
            self.rotation.append(animation)
        if (animation.anim_type == "sk"):
            self.skew.append(animation)
        
    '''
    main function to call that updates keyframe values
    and renders object to screen
    '''
    def updateObject(self, deltaTime):
        self.surface.fill((0, 0, 0))
        x_offset = self.object_rect[0]
        y_offset = self.object_rect[1]
        x = 0
        y = 0
       
        for system in self.position:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        for system in self.scale:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        for system in self.rotation:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        for system in self.skew:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        
        self.surface.blit(self.object, (x_offset, y_offset))
        
    '''
    update/linearly interpolate values based on keyframe's settings
    like easings
    '''
    def animateSystem(self, deltaTime, system):
        key = system.processed_keyframes[system.index]
        if (system.index < len(system.processed_keyframes)):
            
            if (system.argument3):
                if (system.argument1):
                    key.lerpval += deltaTime
                elif (not system.argument1 and key.lerpval > 0):
                    key.lerpval -= deltaTime
            else:
                key.lerpval += deltaTime
                

            key.lerpval = min(key.lerpval, key.length) 
            if (system.index > 0):
                t = key.lerpval / key.length
                t = max(0, min(t, 1))  
            else:
                t = 0
            if (key.easing != "linear"):
                if key.easing == "out_circ":
                    t = np.sqrt(1 - (t - 1) ** 2)
                if key.easing == "in_circ":
                    t = 1 - np.sqrt(1 - (t ** 2))
                if key.easing == "in_out_circ":
                    if (t < 0.5):
                        t = (1 - np.sqrt(1 - (t * 2) ** 2)) / 2
                    else:
                        t = (np.sqrt(1 - ((t * 2) - 1) ** 2) + 1) / 2
                if key.easing == "out_expo":
                    t = 2 ** (10 * (t - 1))
                if key.easing == "in_expo":
                    t = 1 - 2 ** (-10 * t)
                if key.easing == "in_out_expo":
                    if (t < 0.5):
                        t = 2 ** (20 * (t - 10))  
                    else:
                        t = 2 - 2 ** (-20 * (t + 10))
                if key.easing == "out_sine":
                    t = np.sin((t * np.pi) / 2)
                if key.easing == "in_sine":
                    t = 1 - np.cos((t * np.pi) / 2)
                if key.easing == "in_out_sine":
                    t = (1 - np.cos(t * np.pi)) / 2
            if system.index == 0:
                system.value = (key.x2, key.y2)
            else:
                system.value = (system.lerp(key.x1, key.x2, t), system.lerp(key.y1, key.y2, t))

            if (system.argument3):
                if key.lerpval >= key.length and not system.argument1:
                    system.index += 1
                    if system.loop and system.index >= len(system.processed_keyframes):
                        system.index = 0
                        for keys in system.processed_keyframes:
                            keys.lerpval = 0 
                    if system.argument2:
                        system.index = 2
                
            else:
                if key.lerpval >= key.length:
                    system.index += 1
                    if system.loop and system.index >= len(system.processed_keyframes):
                        system.index = 0
                        for keys in system.processed_keyframes:
                            keys.lerpval = 0 
                if system.index >= len(system.processed_keyframes):
                    system.index = len(system.processed_keyframes) - 1
        
        
    
    '''
    draw image on screen based on
    what type it is
    '''
    def calculateTracks(self, system):
        x = 0
        y = 0

        
        if system.anim_type == "p":
            x += system.value[0] 
            y += system.value[1]
        elif system.anim_type == "s":
            self.object = pygame.transform.smoothscale(self.object_copy, (self.object_copy.get_rect()[2] * system.value[0], self.object_copy.get_rect()[3] * system.value[1]))
            x += (self.object_copy.get_rect()[2] - self.object.get_rect()[2]) / 2
            y += (self.object_copy.get_rect()[3] - self.object.get_rect()[3]) / 2
            
        
            
        
        return (x, y)
            
        

'''
def renderObject(self, system):
    x = 0
    y = 0

    if system.anim_type == "p":
        # Get current size of the object
        width, height = self.object.get_rect()[2], self.object.get_rect()[3]

        # Move to position, then offset to center the object
        x = BASE_POS[0] + system.value[0] - width / 2
        y = BASE_POS[1] + system.value[1] - height / 2

    elif system.anim_type == "s":
        # Compute new size based on scale system
        new_width = int(self.object_copy.get_width() * system.value[0])
        new_height = int(self.object_copy.get_height() * system.value[1])

        # Update the scaled object
        self.object = pygame.transform.smoothscale(self.object_copy, (new_width, new_height))

        # To keep it centered, offset by half the change in width/height
        old_width = self.object_copy.get_width()
        old_height = self.object_copy.get_height()

        dx = (old_width - new_width) / 2
        dy = (old_height - new_height) / 2

        x += dx
        y += dy

    return (x, y)
'''
                

'''
animation track class
'''
class animation(object):
    def __init__(self, type, keyframes, origin = (0, 0), does_loop = False, arg1 = False, arg2 = False, arg3 = False):
        self.argument1 = arg1
        self.argument2 = arg2
        self.argument3 = arg3
        self.processed_keyframes = []
        self.index = 0
        self.origin = origin
        self.loop = does_loop
        self.value = self.origin
        self.anim_type = type 
        for i in keyframes:
            if len(i) > 3:
                self.addKeyframe(i[0], i[1], i[2], i[3])
            else:
                self.addKeyframe(i[0], i[1], i[2])
        
        

    

        
            
            
    


    '''
    lerp function for linear interpolation
    '''
    def lerp(self, start, end, t):
        return (1 - t) * start + t * end
    
    '''
    add a new keyframe to an animation track
    '''
    def addKeyframe(self, time, x, y, ease = "linear"):
        new_key = keyframe()
        if len(self.processed_keyframes) > 0:
            new_key.x1 = self.processed_keyframes[-1].x2
            new_key.y1 = self.processed_keyframes[-1].y2
        else:
            new_key.x1 = self.origin[0]
            new_key.y1 = self.origin[1]
        new_key.x2 = x
        if self.anim_type == "p":
            new_key.y2 = -y
        else:
            new_key.y2 = y
        new_key.time = time
        new_key.easing = ease
        new_key.lerpval = 0
        for i in self.processed_keyframes:
            if new_key.time == i:
                new_key.time = i + 0.001
                break
        if len(self.processed_keyframes) > 0:
            new_key.length = new_key.time - self.processed_keyframes[-1].time
        self.processed_keyframes.append(new_key)

'''
keyframe class that contains all the needed info for a keyframe
'''
class keyframe():
    def __init__(self):
        self.lerpval = 0
        self.easing = ""
        self.length = 0
        self.time = 0
        self.x1 = 0
        self.x2 = 0
        self.y1 = 0
        self.y2 = 0
    '''
    left in for debugging
    '''
    def __str__(self):
        return f"x1: {self.x1} x2: {self.x2} y1: {self.y1} y2: {self.y2} time: {self.time} length: {self.length} ease: {self.easing} lerp: {self.lerpval}"
