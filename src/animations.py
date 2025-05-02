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
    def __init__(self, object, screen, origin = (0, 0), is_button = False, is_overlay = False, label = None, label_visibility = True):
        self.label = label
        self.show_label = label_visibility
        self.position = []
        self.scale = []    
        #todo   
        self.rotation = []
        #todo maybe
        self.skew = []
        
        self.opacity = []
        self.attributes = [(0, 0), (0, 0)]
        self.surface = screen
        self.object = object
        self.object_copy = object
        self.object_backup = object
        self.object_rect = pygame.Rect((BASE_POS[0] + origin[0]) - (object.get_rect()[2] / 2), (BASE_POS[1] + (-origin[1])) - (object.get_rect()[3] / 2), object.get_rect()[2], object.get_rect()[3])
        self.object_rect_backup = self.object_rect
        self.is_button = is_button
        self.is_hovering = False
        self.l_mouse_down = False

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
        if (animation.anim_type == "p"):
            self.position.append(animation)
        if (animation.anim_type == "s"):
            self.scale.append(animation)
        if (animation.anim_type == "r"):
            self.rotation.append(animation)
        if (animation.anim_type == "sk"):
            self.skew.append(animation)
        if (animation.anim_type == "o"):
            self.opacity.append(animation)
        
    '''
    main function to call that updates keyframe values
    and renders object to screen
    '''
    def updateObject(self, deltaTime, active_popups, blit = True):
        
        x_offset = self.object_rect[0]
        y_offset = self.object_rect[1]
        x = 0
        y = 0
        if self.is_button:
            if active_popups == 0:
                if (self.object_rect.collidepoint(pygame.mouse.get_pos())):
                    
                    self.is_hovering = True
                else:
                    self.is_hovering = False
            else:
                self.is_hovering = False
        else:
            if (self.object_rect.collidepoint(pygame.mouse.get_pos())):    
                self.is_hovering = True
            else:
                self.is_hovering = False
        for system in self.position:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        self.attributes[0] = (x_offset, y_offset)
        for system in self.scale:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        self.attributes[1] = (x_offset, y_offset)
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
        for system in self.opacity:
            self.animateSystem(deltaTime, system)
            (x, y) = self.calculateTracks(system)
            x_offset += x
            y_offset += y
        if blit:
            self.surface.blit(self.object, (x_offset, y_offset))
            if self.label != None and self.show_label == True:
                self.surface.blit(self.label, (self.object_rect[0] + (self.object_rect[0] - x_offset) + (self.object.get_size()[0]) + 10, self.object_rect_backup[1] + (self.object_rect_backup[3] / 2) - self.label.get_size()[1]/2))
                
               
                
        else:
            return (x_offset, y_offset)
        
    '''
    update/linearly interpolate values based on keyframe's settings
    like easings
    '''
    def animateSystem(self, deltaTime, system):
        key = system.processed_keyframes[system.index]
        if (system.index < len(system.processed_keyframes)):
            
            if (self.is_button):
                if (self.is_hovering and not self.l_mouse_down):
                    system.index = 1
                    key.lerpval += deltaTime
                    key = system.processed_keyframes[system.index]
                    
                elif (key.lerpval > 0 and self.is_hovering == False and not self.l_mouse_down):
                    key.lerpval -= deltaTime
                    key = system.processed_keyframes[system.index]
                    
                
                
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

            
                
            if (self.is_button == False):
                if (key.lerpval >= key.length):
                    system.index += 1
                    if system.loop and system.index >= len(system.processed_keyframes):
                        system.index = 0
                        for keys in system.processed_keyframes:
                            keys.lerpval = 0 
                if system.index >= len(system.processed_keyframes):
                    system.index = len(system.processed_keyframes) - 1
            elif (self.is_button):  
                if (not self.is_hovering and key.lerpval <= 0 and not self.l_mouse_down):
                    system.index = 0
                    key = system.processed_keyframes[system.index]
                if (self.l_mouse_down):
                    system.index = 2
                    key = system.processed_keyframes[system.index]

                    
                
    def warp_surface(self, surface, angle_y, angle_x):
        width, height = surface.get_size()
        src_rgb = pygame.surfarray.array3d(surface)
        src_alpha = pygame.surfarray.array_alpha(surface)

        x = np.linspace(-1, 1, width)
        y = -np.linspace(-1, 1, height)
        xv, yv = np.meshgrid(x, y)
        zv = np.zeros_like(xv)

        rad_x = np.radians(angle_x)
        yv_rot = yv * np.cos(rad_x) - zv * np.sin(rad_x)
        zv = yv * np.sin(rad_x) + zv * np.cos(rad_x)

       
        rad_y = np.radians(angle_y)
        xv_rot = xv * np.cos(rad_y) + zv * np.sin(rad_y)
        zv = -xv * np.sin(rad_y) + zv * np.cos(rad_y)

        fov = 8
        zv_persp = zv + fov
        xv_proj = xv_rot / zv_persp
        yv_proj = yv_rot / zv_persp

  
        xv_px = ((xv_proj - xv_proj.min()) / (xv_proj.max() - xv_proj.min()) * (width - 1)).astype(np.int32)
        yv_px = ((yv_proj - yv_proj.min()) / (yv_proj.max() - yv_proj.min()) * (height - 1)).astype(np.int32)

       
        xv_px = np.clip(xv_px, 0, width - 1)
        yv_px = np.clip(yv_px, 0, height - 1)

        warped_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        warped_rgb = np.zeros((width, height, 3), dtype=np.uint8)
        warped_alpha = np.zeros((width, height), dtype=np.uint8)

        for y in range(height):
            for x in range(width):
                src_x = xv_px[y, x]
                src_y = yv_px[y, x]
                warped_rgb[x, y] = src_rgb[src_x, src_y]
                warped_alpha[x, y] = src_alpha[src_x, src_y]

     
        pygame.surfarray.blit_array(warped_surface, warped_rgb)
        pygame.surfarray.pixels_alpha(warped_surface)[:, :] = warped_alpha

        return warped_surface


        
        
    
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
        elif system.anim_type == "r":
            self.object = pygame.transform.rotate(self.object_copy, system.value[0])
            
            x += (self.object_copy.get_rect()[2] - self.object.get_rect()[2]) / 2
            y += (self.object_copy.get_rect()[3] - self.object.get_rect()[3]) / 2
        elif system.anim_type == "sk":
            if self.object_rect.collidepoint(pygame.mouse.get_pos()):
                
                self.object = self.warp_surface(self.object_copy, (pygame.mouse.get_pos()[0] - self.object_rect[0] - (self.object_rect[2] / 2)) * 1.25, (pygame.mouse.get_pos()[1] - self.object_rect[1] - (self.object_rect[3]) / 2) * 1.25)
                

                x += (pygame.mouse.get_pos()[0] - self.object_rect[0] - (self.object_rect[2] / 2)) / 10
                y += (pygame.mouse.get_pos()[1] - self.object_rect[1] - (self.object_rect[3] / 2)) / 10
                
                
                
                
                
            
                
                

                
            else: 
                self.object = self.object_backup
                self.object_rect = self.object_rect_backup
                
        elif system.anim_type == "o":
            pass
        
            
        
        return (x, y)
    
 
            
        

                

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
        if self.anim_type == "o":
            new_key.y1 = 0
            new_key.y2 = 0

        self.processed_keyframes.append(new_key)
    
    def __str__(self):
        return self.processed_keyframes[0]
    
    

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
