import pygame
import os
import numpy as np
import pyautogui
from PIL import Image
import io
import animations as anim

src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = f'{project_dir}\\textures\\'
data_dir = f'{project_dir}\\data\\'

class button:
    def __init__(self, texture, screen, callback, pos, animation_length, scale_to):
        self.hover = False
        self.callback = callback
        self.length = animation_length
        self.clicked = False
        self.animation_base = anim.object(pygame.image.load(f'{textures_dir}{texture}.png').convert_alpha(), screen, pos, is_button = True)
        self.animation_base.addAnimationTrack("s", [[0, 1, 1], [animation_length, scale_to, scale_to, "out_circ"], [0.05, scale_to - 0.1, scale_to - 0.1, "out_circ"]])
        print(self.animation_base.scale.__str__())
        


class blank_popup:
    def __init__(self, screen, type, buttons, x, y, animation_length, scale_to, close_callback):
        if len(buttons) > 0:
            pass
        self.buttons = []
        self.active = False
        self.length = animation_length
        self.origin = (x, y)
        self.surface = screen
        img = pygame.image.load(f'{textures_dir}popup_blank.png').convert_alpha()
        self.popup_animation_base = anim.object(img, screen, (x, y), is_button = False)
        #self.popup_animation_base.addAnimationTrack("s", [[0, 0, 0], [animation_length, scale_to, scale_to, "out_circ"], [0.05, 1, 1, "out_circ"]])
        #img_size = (img.get_height(), img.get_width())
        self.create_button(close_callback, "exit", (200, 0), scale = 1.15, animation_length = 0.08)
        self.overlay = anim.object(pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA), screen, (0, 0), False, is_overlay = True)
        self.overlay = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(0)
        
        self.graph = []
    
    def create_button(
            self,
            callback,                  
            texture,    
            pos = (0, 0),                      
            layout = (-1, -1),                
            scale = 1.15,                  
            animation_length = 0.08     
            ):
        
        temp_button = button(texture, self.surface, callback, pos, animation_length, scale)
        if (layout[0] != -1): #column
            if (len(self.buttons) > 0):
                temp_button.animation_base.object_rect[0] = (((self.buttons[-1].animation_base.object_rect[2]) + self.buttons[-1].animation_base.object_rect[0]) * layout[0]) + 35
                
        if (layout[1] != -1): #row
            if (len(self.buttons) > 0):
                temp_button.animation_base.object_rect[1] = (((self.buttons[-1].animation_base.object_rect[3]) + self.buttons[-1].animation_base.object_rect[1]) * layout[1]) + 35
       
            
        self.buttons.append(temp_button)
        
        
        



class gui_screen:
    def __init__(self, screen, page = 0, active = True):
        self.page = page
        self.prio_queue = []
        self.buttons = []
        self.popups = []
        self.surface = screen
        self.active = active

    def create_static_texture(self, texture, pos = (0, 0)):
        tex = pygame.image.load(f'{textures_dir}{texture}.png').convert_alpha()
        tex_rect = pygame.Rect(pos[0], pos[1], tex.get_rect()[2], tex.get_rect()[3])
        self.prio_queue.append((tex, tex_rect))

    def update_prio_queue(self):
        if len(self.prio_queue) > 0:
            for tx in self.prio_queue:
                self.surface.blit(tx[0], tx[1])

    def create_button(
            self,
            callback,                  
            texture,    
            pos = (0, 0),                      
            layout = (-1, -1),                
            scale = 1.15,                  
            animation_length = 0.08     
            ):
        
        temp_button = button(texture, self.surface, callback, pos, animation_length, scale)
        if (layout[0] != -1): #column
            if (len(self.buttons) > 0):
                temp_button.animation_base.object_rect[0] = (((self.buttons[-1].animation_base.object_rect[2]) + self.buttons[-1].animation_base.object_rect[0]) * layout[0]) + 35
                
        if (layout[1] != -1): #row
            if (len(self.buttons) > 0):
                temp_button.animation_base.object_rect[1] = (((self.buttons[-1].animation_base.object_rect[3]) + self.buttons[-1].animation_base.object_rect[1]) * layout[1]) + 35
       
            
        self.buttons.append(temp_button)
        

    def create_graph_popup(self, data):
        tmp_popup = blank_popup(self.surface, "g", [], 0, 0, 0, 1, self.kill_popup)
        
        if data != []:
            index = 0
            for y in data:
                dot = anim.object(pygame.image.load(f"{textures_dir}dot.png"), self.surface, ((((400 // len(data)) * index) - 200), -100), False)
                dot.addAnimationTrack("p", [[0, 0, 0], [0.25, 0, 0], [0.75, 0, (y * 2), "in_out_sine"]])
                index += 1
                tmp_popup.graph.append(dot)
        tmp_popup.active = True
        self.popups.append(tmp_popup)
       

    


    def kill_popup(self):
        del self.popups[-1]


    

    
    def update(self, deltatime, event1, event2, screen, frame = None, boxes = None):
        
        if self.page == screen:
            active_popups = 0

            for popup in self.popups:
                if popup.active:
                    active_popups += 1
                else:
                    break
            if (active_popups == 0):
                
                for button in self.buttons:
                    if button.animation_base.object_rect.collidepoint(pygame.mouse.get_pos()) and self.active:
                        button.hover = True
                    else:
                        button.hover = False
                


                for button in self.buttons:
                    if (button.hover and (event1 or button.clicked)):
                        button.clicked = True
                        button.animation_base.l_mouse_down = True
                        
                        if event2:
                                button.animation_base.l_mouse_down = False
                                button.clicked = False
                                event2 = False
                                event1 = False
                                button.hover = False
                                button.callback()
                                
                    else:
                        button.animation_base.l_mouse_down = False
                        button.clicked = False
            

            else:
                for button in self.buttons:
                    button.clicked = False
            if len(self.prio_queue) > 0:
                for prio in self.prio_queue:
                    self.surface.blit(prio[0], prio[1])
            else:
                self.surface.fill((0, 0, 0))
            for button in self.buttons:
                button.animation_base.updateObject(deltatime, active_popups)
            for popup in self.popups:
                if popup.active:
                    
                    for button in popup.buttons:
                      
                        if button.animation_base.object_rect.collidepoint(pygame.mouse.get_pos()):
                            button.hover = True
                        else:
                            button.hover = False


                    for button in popup.buttons:
                        if (button.hover and (event1 or button.clicked)):
                            button.clicked = True
                            button.animation_base.l_mouse_down = True
                            
                            if event2:
                                    button.animation_base.l_mouse_down = False
                                    button.clicked = False
                                    event2 = False
                                    event1 = False
                                    button.hover = False
                                    button.callback()
                                    
                        else:
                            button.animation_base.l_mouse_down = False
                            button.clicked = False
                    


                    popup.popup_animation_base.updateObject(deltatime, active_popups)
                    for button in popup.buttons:
                        
                        button.animation_base.updateObject(deltatime, active_popups)
                    index = 0
                    for point in popup.graph:
                        point.updateObject(deltatime, active_popups)
                        if index < len(popup.graph) - 1:
                            pygame.draw.line(self.surface, (255, 255, 255), (point.attributes[0][0] + (point.object_rect[2] // 2), point.attributes[0][1] + (point.object_rect[3] // 2)), (popup.graph[index + 1].attributes[0][0] + (popup.graph[index + 1].object_rect[2] // 2), popup.graph[index + 1].attributes[0][1] + (popup.graph[index + 1].object_rect[3] // 2)))
                        index += 1
                   
                        
                else:
                    break
                

            
    def update_popups(self, dt, event1, event2):
        for popup in self.popups:
            if popup.active:
                pass
            else:
                break

    


screens = {
    "home": 0,
    "settings": 1
}

#animations
def out_circ(t):
    return np.sqrt(1 - (t - 1) ** 2)

def lerp(start, end, t):
  return (1 - t) * start + t * end
