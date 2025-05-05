import pygame
import os
import numpy as np
import pyautogui
from PIL import Image
import io
import animations as anim

src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = os.path.join(project_dir, 'textures')
data_dir = os.path.join(project_dir, "data")

class label:
    def __init__(self, surface, text, pos, does_change = False, data = None):
        if data != None:
            self.label = anim.object(pygame.font.Font(None, 24).render(text + f' {data:.2f}', True, (255, 255, 255)), surface, pos, does_change=does_change)
        else:
            self.label = anim.object(pygame.font.Font(None, 24).render(text, True, (255, 255, 255)), surface, pos,does_change=does_change)
        self.data = data
        self.text = text
        self.swaps = does_change

    def update_data(self, new_data, new_text = None):
        if new_text == None:
            new_text = self.text
        self.label.update_surface(pygame.font.Font(None, 24).render(new_text + f' {new_data:.2f}', True, (255, 255, 255)))

class button:
    def __init__(self, texture, screen, callback, pos, animation_length, scale_to, toggle = False, extra_text = None):
        
        self.hover = False
        self.callback = callback
        self.length = animation_length
        self.clicked = False
        surf = pygame.image.load(os.path.join(textures_dir, texture + '.png')).convert_alpha()

        if extra_text != None:
       
            text = pygame.font.Font(None, 24).render(extra_text, True, (255, 255, 255))
            
          
        else:
            text = None
        
        self.animation_base = anim.object(surf, screen, pos, is_button = True, label=text)
        self.animation_base.addAnimationTrack("s", [[0, 1, 1], [animation_length, scale_to, scale_to, "out_circ"], [0.05, scale_to - 0.1, scale_to - 0.1, "out_circ"]])
        if toggle == True:
            self.toggle_on = pygame.image.load(os.path.join(textures_dir, "tick_filled" + '.png')).convert_alpha()
            self.toggle_off = pygame.image.load(os.path.join(textures_dir, "tick_empty" + '.png')).convert_alpha()
            self.toggle = toggle
            
        else:
            self.toggle = False
        
        
        #print(self.animation_base.scale.__str__())
        


class blank_popup:
    def __init__(self, screen, type, buttons, x, y, animation_length, scale_to, close_callback):
        if len(buttons) > 0:
            pass
        self.buttons = []
        self.active = False
        self.length = animation_length
        self.origin = (x, y)
        self.surface = screen
        img = pygame.image.load(os.path.join(textures_dir, 'popup_blank.png')).convert_alpha()
        self.img = img
        self.popup_animation_base = anim.object(img, screen, (x, y), is_button = False)
        self.popup_animation_base.addAnimationTrack("s", [[0, 0.5, 0.5]])
        #img_size = (img.get_height(), img.get_width())
        self.create_button(close_callback, "exit", (-410 / 2, 205 / 2), scale = 0.8, animation_length = 0.08)
        self.overlay = anim.object(pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA), screen, (0, 0), False, is_overlay = True)
        self.overlay = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0))
        self.overlay.set_alpha(0)
        self.data = None
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
        self.labels = []
       
        self.popups = []
        self.surface = screen
        self.active = active

    def create_static_texture(self, texture, pos = (0, 0)):
        tex = pygame.image.load(os.path.join(textures_dir, f'{texture}.png')).convert_alpha()
        tex_rect = pygame.Rect(pos[0], pos[1], tex.get_rect()[2], tex.get_rect()[3])
        self.prio_queue.append((tex, tex_rect))

    def update_prio_queue(self):
        if len(self.prio_queue) > 0:
            for tx in self.prio_queue:
                self.surface.blit(tx[0], tx[1])

    def create_label(self, text, pos, does_change = False, data = 0):
        self.labels.append(label(self.surface, text, pos, does_change, data))

    def create_button(
            self,
            callback,                  
            texture,    
            pos = (0, 0),                      
            layout = (-1, -1),                
            scale = 1.15,                  
            animation_length = 0.08,
            is_toggle = False,
            with_text = None 
            ):
        
        temp_button = button(texture, self.surface, callback, pos, animation_length, scale, is_toggle, extra_text=with_text)
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
            tmp_popup.data = data
            max_y = max(data)
            normalized_y = [y / max_y for y in data]
            for y in normalized_y:
                dot = anim.object(pygame.image.load(os.path.join(textures_dir, 'dot.png')), self.surface, ((((700 // len(data)) * index) - 350) / 2, -100), False)
                dot.addAnimationTrack("p", [[0, 0, 0], [0.25, 0, 0], [0.75, 0, (y * 200), "out_sine"]])
                index += 1
                tmp_popup.graph.append(dot)
        tmp_popup.active = True
        self.popups.append(tmp_popup)
       

    


    def kill_popup(self):
        del self.popups[-1]


    

    
    def update(self, deltatime, event1, event2, screen, frame = None, boxes = None, toggle_states = []):
        
        if self.page == screen:
            active_popups = 0
            

            for popup in self.popups:
                if popup.active:
                    active_popups += 1
                else:
                    break
            
            if (active_popups == 0):
                if toggle_states != []:
                    tog_index = 0
                    for i in range(len(self.buttons)):
                        if self.buttons[i].toggle:
                            
                            if toggle_states[tog_index] == True:
                                self.buttons[i].animation_base.object = pygame.image.load(os.path.join(textures_dir, "tick_filled" + '.png')).convert_alpha()
                                self.buttons[i].animation_base.object_copy = self.buttons[i].animation_base.object
                                self.buttons[i].animation_base.object_backup = self.buttons[i].animation_base.object
                            else:
                                self.buttons[i].animation_base.object = pygame.image.load(os.path.join(textures_dir, "tick_empty" + '.png')).convert_alpha()
                                self.buttons[i].animation_base.object_copy = self.buttons[i].animation_base.object
                                self.buttons[i].animation_base.object_backup = self.buttons[i].animation_base.object
                            tog_index += 1
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
            for label in self.labels:
                
                        
                label.label.updateObject(deltatime, active_popups)
            for button in self.buttons:
                button.animation_base.updateObject(deltatime, active_popups)
            if frame != None:
                self.surface.blit(frame, (640/4, 360/4))
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
                        expanded_rect = pygame.Rect(point.object_rect[0] - (10), 0, point.object_rect[2] + 20, 640)
                        shrunk_rect = pygame.Rect(popup.popup_animation_base.object_rect[0] + (popup.popup_animation_base.object_rect[2] / 4), popup.popup_animation_base.object_rect[1] + (popup.popup_animation_base.object_rect[3] / 4), popup.popup_animation_base.object_rect[2] / 2, popup.popup_animation_base.object_rect[3] / 2)
                        if expanded_rect.collidepoint(pygame.mouse.get_pos()):
                            
                            text = pygame.font.Font(None, 24).render(str(popup.data[index]), True, (255, 255, 255))
                            self.surface.blit(text, (pygame.mouse.get_pos()[0] + (text.get_size()[0] // 2), pygame.mouse.get_pos()[1] - (text.get_size()[1] // 2)))
                            
                        if shrunk_rect.collidepoint(pygame.mouse.get_pos()):
                            pygame.draw.line(self.surface, (255, 255, 255), (pygame.mouse.get_pos()[0], (popup.img.get_size()[1] / 2)), pygame.mouse.get_pos())
                        point.updateObject(deltatime, active_popups)
                        if index < len(popup.graph) - 1:
                            pygame.draw.line(self.surface, (255, 255, 255), (point.attributes[0][0] + (point.object_rect[2] // 2), point.attributes[0][1] + (point.object_rect[3] // 2)), (popup.graph[index + 1].attributes[0][0] + (popup.graph[index + 1].object_rect[2] // 2), popup.graph[index + 1].attributes[0][1] + (popup.graph[index + 1].object_rect[3] // 2)))
                            pygame.draw.line(self.surface, (255, 255, 255), (popup.graph[0].attributes[0][0] + (popup.graph[0].object_rect[2] // 2), popup.img.get_size()[1] / 2), (popup.graph[-1].attributes[0][0] + (popup.graph[-1].object_rect[2] // 2), popup.img.get_size()[1] / 2))
                            
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
