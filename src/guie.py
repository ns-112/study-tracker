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
popup_dir = os.path.join(textures_dir,'popup')

class button:
    def __init__(self, texture, callback, x = 0, y = 0, column = 0, row = 0, scale = 1, animation_length = 0.5):
        self.base = pygame.image.load(os.path.join(textures_dir,texture)+'.png').convert_alpha()
        self.scale = (pygame.Surface.get_width(self.base) * scale, pygame.Surface.get_height(self.base) * scale)
        self.copy = self.base.convert_alpha()
        self.lerp = 0

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
       


    def create_popup_button(self, text, index, width, height, scale, popup, pyfont = None, color = (255, 255, 255)):
        side_left = pygame.image.load(os.path.join(popup_dir,'text_button_side.png')).convert_alpha()
        side_right_pil = Image.open(os.path.join(popup_dir,'text_button_side.png')).convert("RGBA")
        middle_part = pygame.image.load(os.path.join(popup_dir,'text_button_middle.png')).convert_alpha()
        side_right_pil = side_right_pil.transpose(Image.FLIP_LEFT_RIGHT)
        side_right_bytes = io.BytesIO()
        side_right_pil.save(side_right_bytes, format="PNG")
        side_right_bytes.seek(0)
        side_right = pygame.image.load(side_right_bytes).convert_alpha()

        font = pygame.font.Font(pyfont, 36)

        button_text_surface = font.render(text, True, color)

        button_text_width = button_text_surface.get_width()

        side_width = side_left.get_width()
        side_height = side_left.get_height()

        middle_part_width = button_text_width 

        middle_part_scaled = pygame.transform.scale(middle_part, (button_text_width, side_height))

        button_width = side_width * 2 + middle_part_width * scale 
        button_height = side_height * scale 

        button = pygame.Surface((button_width, button_height))

        button.blit(side_left, (0, 0))

        middle_part_x = side_width
        button.blit(middle_part_scaled, (middle_part_x, 0))

        button.blit(side_right, (side_width + middle_part_width, 0))
  
        text_x = side_width + (middle_part_width - button_text_width) // 2
        text_y = (button_height - button_text_surface.get_height()) // 2
        button.blit(button_text_surface, (text_x, text_y))

        #set the center to 1/4 + 1/8 of popup   or 3/4 + 1/8 of popup
        if (index == 0):
                button_rect = pygame.Rect(
                    ((pygame.Surface.get_width(popup) // 4) + (pygame.Surface.get_width(popup) // 8)) - (pygame.Surface.get_width(button) / 2) + pygame.Surface.get_width(popup) // 4, 
                    pygame.display.get_surface().get_size()[1] // 2 + pygame.display.get_surface().get_size()[1] // 6, 
                    button_width, 
                    button_height
                    )
        else:
                button_rect = pygame.Rect(
                    (((pygame.Surface.get_width(popup) // 4) * 3) + (pygame.Surface.get_width(popup) // 8)) - (pygame.Surface.get_width(button) / 2)  + pygame.Surface.get_width(popup) // 4, 
                    pygame.display.get_surface().get_size()[1] // 2 + pygame.display.get_surface().get_size()[1] // 6, 
                    button_width, 
                    button_height
                )

        
        
        return button, (button_rect[0], button_rect[1])

    def create_basic_popup(self, width, height, button_1_callback, button_2_callback, name="popup", popup_text="this is a popup.", button_1_name="okay", button_2_name="cancel", animation_length=0.5, button_scale=1):


        popup_base = pygame.Surface((width, height))
        popup_base.fill((110, 110, 110))


        button_1, pos1 = self.create_popup_button(button_1_name, 0, width, height, button_scale, popup_base)
        button_1_size = (pygame.Surface.get_width(button_1) * button_scale, pygame.Surface.get_height(button_1) * button_scale)
        button_1_rect = button_1.get_rect()
        button_1_rect.width = button_1_size[0]
        button_1_rect.height = button_1_size[1]


        if pos1[0] <= button_1_size[0]:
            pos1[0] = (button_1_size[0] / 2) + 5
        if pos1[1] <= button_1_size[1]:
            pos1[1] = (button_1_size[1] / 2) + 5


        button_1_rect = pygame.Rect(abs(pos1[0]), abs(pos1[1]), button_1_size[0], button_1_size[1])
        original_pos_1 = pos1
        clicked_on = False
        scaled_1_rect = pygame.Rect(button_1_rect[2], button_1_rect[3], button_1_size[0], button_1_size[1])
        button_1_copy = button_1

        button_2, pos2 = self.create_popup_button(button_2_name, 1, width, height, button_scale, popup_base)
        button_2_size = (pygame.Surface.get_width(button_2) * button_scale, pygame.Surface.get_height(button_2) * button_scale)
        
        button_2_rect = button_2.get_rect()
        button_2_rect.width = button_2_size[0]
        button_2_rect.height = button_2_size[1]


        if pos2[0] <= button_2_size[0]:
            pos2[0] = (button_2_size[0] / 2) + 5
        if pos2[1] <= button_2_size[1]:
            pos2[1] = (button_2_size[1] / 2) + 5


        button_2_rect = pygame.Rect(abs(pos2[0]), abs(pos2[1]), button_2_size[0], button_2_size[1])
        original_pos_2 = pos2
        clicked_on = False
        scaled_2_rect = pygame.Rect(button_2_rect[2], button_2_rect[3], button_2_size[0], button_2_size[1])
        button_2_copy = button_2

        font = pygame.font.Font(None, 36)
        popup_text_render = font.render(popup_text, True, (255, 255, 255))

        overlay = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0))
        overlay.set_alpha(0)

        

        if button_1_callback is None:
            button_1_callback = self.kill_popup

        button_1_attributes = [
            button_1,
            0,
            False,
            button_1_callback,
            button_1_size,
            button_1_rect,
            button_1_copy,
            animation_length,
            scaled_1_rect,
            original_pos_1,
            clicked_on
        ]
        button_2_attributes = [
            button_2,
            0,
            False,
            button_2_callback,
            button_2_size,
            button_2_rect,
            button_2_copy,
            animation_length,
            scaled_2_rect,
            original_pos_2,
            clicked_on
        ]
        
        self.active_popups[name] = [
            button_1_attributes,
            button_2_attributes,
            overlay,
            popup_base,
            popup_text_render,
            0,
            animation_length,
            0

        ]


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
            if frame != None:
                self.surface.blit(frame, (1280/4, 720/4))
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
