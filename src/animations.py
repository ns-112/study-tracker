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
    def addAnimationTrack(self, type, keyframes, start = (0, 0), loop = False):
        anim = animation(type, keyframes, origin = start, does_loop = loop)
        self.addAnimationFromClass(anim)
    

    '''
    add animation system to main object's list of references.
    this allows the user to add multiple animation tracks of the same type, hopefully
    allowing for some interesting animations
    '''
    def addAnimationFromClass(self, animation):
        if (animation.anim_type == "position"):
            self.position.append(animation)
        if (animation.anim_type == "scale"):
            self.scale.append(animation)
        if (animation.anim_type == "rotation"):
            self.rotation.append(animation)
        if (animation.anim_type == "skew"):
            self.skew.append(animation)
        
    '''
    main function to call that updates keyframe values
    and renders object to screen
    '''
    def updateObject(self, deltaTime):
        self.surface.fill((0,0,0))
        for system in self.position:
            self.animateSystem(deltaTime, system)
            self.renderObject(system)
        for system in self.scale:
            self.animateSystem(deltaTime, system)
            self.renderObject(system)
        for system in self.rotation:
            self.animateSystem(deltaTime, system)
            self.renderObject(system)
        for system in self.skew:
            self.animateSystem(deltaTime, system)
            self.renderObject(system)
        
    '''
    update/linearly interpolate values based on keyframe's settings
    like easings
    '''
    def animateSystem(self, deltaTime, system):
        key = system.processed_keyframes[system.index]
        if (system.index < len(system.processed_keyframes)):
            
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
            if key.lerpval >= key.length:
                system.index += 1
                if system.loop and system.index >= len(system.processed_keyframes):
                    system.index = 0
                    for keys in system.processed_keyframes:
                        keys.lerpval = 0 
    
    '''
    draw image on screen based on
    what type it is
    '''
    def renderObject(self, system):
        if system.anim_type == "position":
            system.surface.blit(self.object, ((BASE_POS[0] + self.object.get_rect()[2] / 2) + system.value[0], (BASE_POS[1] + self.object.get_rect()[3] / 2) + system.value[1]))
        elif system.anim_type == "scale":
            self.object = pygame.transform.smoothscale(self.object_copy, (self.object_copy.get_rect()[2] * system.value[0], self.object_copy.get_rect()[3] * system.value[1]))
            self.surface.blit(self.object, (self.object_rect[0] - (self.object.get_rect()[2] / 2), self.object_rect[1] - (self.object.get_rect()[3] / 2)))

            
                

'''
animation track class
'''
class animation(object):
    def __init__(self, type, keyframes, origin = (0, 0), does_loop = False):
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
    def addKeyframe(self, time, x, y, ease="linear"):
        new_key = keyframe()
        if len(self.processed_keyframes) > 0:
            new_key.x1 = self.processed_keyframes[-1].x2
            new_key.y1 = self.processed_keyframes[-1].y2
        else:
            new_key.x1 = self.origin[0]
            new_key.y1 = self.origin[1]
        new_key.x2 = x
        if self.anim_type == "position":
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
