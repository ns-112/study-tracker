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

class button:
    def __init__(self, texture, screen, callback, x, y, animation_length, scale_to):
        self.hover = False
        self.callback = callback
        self.length = animation_length
        self.clicked = False
        self.animation_base = anim.object(pygame.image.load(f'{textures_dir}{texture}.png').convert_alpha(), screen, (x, y), is_button = True)
        self.scale_track = self.animation_base.addAnimationTrack("s", [[0, 1, 1], [animation_length, scale_to, scale_to, "out_circ"], [0.05, scale_to - 0.1, scale_to - 0.1, "out_circ"]], )
        
class popup:
    def __init__(self, button1_text, button2_text, button1_callback, button2_callback, x, y, animation_length):
        self.active = False
        self.length = animation_length
        self.popup = None
        self.button1 = gui_screen.create_popup_button(self, button1_text, 0, popup = self.popup)



class gui_screen:
    def __init__(self, screen, page = 0, active = True):
        self.page = page
        self.prio_queue = []
        self.buttons = []
        self.active_popups = {}
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
            screen,
            callback,                  
            texture,    
            x = 0,                     
            y = 0,                      
            layout = (-1, -1),                
            scale = 1.15,                  
            animation_length = 0.08     
            ):
        
        temp_button = button(texture, screen, callback, x, y, animation_length, scale)
        if (layout[0] != -1): #column
            if (len(self.buttons) > 0):
                temp_button.animation_base.object_rect[0] = (((self.buttons[-1].animation_base.object_rect[2]) + self.buttons[-1].animation_base.object_rect[0]) * layout[0]) + 35
                
        if (layout[1] != -1): #row
            if (len(self.buttons) > 0):
                temp_button.animation_base.object_rect[1] = (((self.buttons[-1].animation_base.object_rect[3]) + self.buttons[-1].animation_base.object_rect[1]) * layout[1]) + 35
        print(temp_button.animation_base.object_rect)
            
        self.buttons.append(temp_button)
        

    def create_graph_popup(self, width, height):
        pass

    def create_popup_button(self, text, index, width, height, scale, popup, pyfont = None, color = (255, 255, 255)):
        side_left = pygame.image.load(f'{textures_dir}\\popup\\text_button_side.png').convert_alpha()
        side_right_pil = Image.open(f'{textures_dir}\\popup\\text_button_side.png').convert("RGBA")
        middle_part = pygame.image.load(f'{textures_dir}\\popup\\text_button_middle.png').convert_alpha()
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
        popup_text_render = font.render(popup_text, True, (255, 255, 255)).convert_alpha()

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

        del self.active_popups
        self.active_popups = {}

    

    
    def update(self, deltatime, event1, event2, screen, frame = None, boxes = None):
        
        if self.page == screen:
            if (len(self.active_popups) == 0):
                
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
                button.animation_base.updateObject(deltatime, self.active_popups)
                

            
            '''
             if (len(self.active_popups) == 0):
                #click
                for button in self.buttons:
                    if (button.hover and (event1 or button.clicked)):
                        button.clicked = True
                        t = button.lerp / (button.length / 10)
                        t = max(0, min(t, 1))  
                        eased_t = out_circ(t)
                        new_width = lerp(button.scale[0], button.scale[0] * 1.1, eased_t)
                        new_height = lerp(button.scale[1], button.scale[1] * 1.1, eased_t)
                        button.base = pygame.transform.smoothscale(button.copy, (int(new_width), int(new_height)))
                        center = button.base.get_rect().center
                        button.rect = pygame.Rect(button.pos[0] - ((button.base.get_rect()[2] - button.scale[0]) / 2), button.pos[1] - ((button.base.get_rect()[3] - button.scale[1]) / 2), button.rect[2], button.rect[3])

                        if event2:
                            button.clicked = False
                            event2 = False
                            event1 = False
                            button.hover = False
                            button.callback()
                    else:
                        button.clicked = False
            else:
                for button in self.buttons:
                    button.clicked = False
            '''
           
                
            


            #render
            '''
            self.surface.fill((0, 0, 0))
            if self.page == 2 and frame is not None:
                self.surface.blit(frame, (frame.get_width() / 2, frame.get_height() / 4))

            for button in self.buttons:
                
                self.surface.blit(button.base, button.rect)
            '''
            
        

    def update_active_popups(self, dt, event1, event2):
        

        
        # Fade overlay in popups
        for name, data in self.active_popups.items():
            if data[5] < data[6]:
                data[5] += dt
            if data[6] < 128:
                t = data[5] / (data[6])
                t = max(0, min(t, 1))
                eased_t = out_circ(t)
                data[7] = lerp(0, 128, eased_t)
                data[2].set_alpha(data[7])

        #hover
            for name, data in self.active_popups.items():
                if pygame.Rect(data[0][9][0] - (data[0][6].get_rect()[2] //2), data[0][9][1] - (data[0][6].get_rect()[3] // 2), data[0][4][0], data[0][4][1]).collidepoint(pygame.mouse.get_pos()) and self.active:
                    data[0][2] = True
                else:
                    data[0][2] = False

                if pygame.Rect(data[1][9][0] - (data[1][6].get_rect()[2] //2), data[1][9][1] - (data[1][6].get_rect()[3] // 2), data[1][4][0], data[1][4][1]).collidepoint(pygame.mouse.get_pos()) and self.active:
                    data[1][2] = True
                else:
                    data[1][2] = False
            
            for name, data in self.active_popups.items():
                if data[0][2]:
                    if data[0][1] < (data[0][7] / 10):
                    
                        data[0][1] += dt
                else:
                    if data[0][1] > 0:
                        data[0][1] -= dt
                
                if data[1][2]:
                    if data[1][1] < (data[1][7] / 10):
                    
                        data[1][1] += dt
                else:
                    if data[1][1] > 0:
                        data[1][1] -= dt
        

         #hover scale
        for name, data in self.active_popups.items():
            t = data[0][1] / (data[0][7] / 10)
            t = max(0, min(t, 1))  
            eased_t = out_circ(t)
            new_width = lerp(data[0][4][0], data[0][4][0] * 1.25, eased_t)
            new_height = lerp(data[0][4][1], data[0][4][1] * 1.25, eased_t)
            data[0][0] = pygame.transform.smoothscale(data[0][6], (int(new_width), int(new_height)))
            data[0][8] = data[0][0].get_rect().center
            data[0][5] = pygame.Rect((data[0][0].get_rect()[0] - (data[0][8][0])) + data[0][9][0], (data[0][0].get_rect()[1] - (data[0][8][1])) + data[0][9][1], data[0][5][2], data[0][5][3]) 
            
            t = data[1][1] / (data[1][7] / 10)
            t = max(0, min(t, 1))  
            eased_t = out_circ(t)
            new_width = lerp(data[1][4][0], data[1][4][0] * 1.25, eased_t)
            new_height = lerp(data[1][4][1], data[1][4][1] * 1.25, eased_t)
            data[1][0] = pygame.transform.smoothscale(data[1][6], (int(new_width), int(new_height)))
            data[1][8] = data[1][0].get_rect().center
            data[1][5] = pygame.Rect((data[1][0].get_rect()[0] - (data[1][8][0])) + data[1][9][0], (data[1][0].get_rect()[1] - (data[1][8][1])) + data[1][9][1], data[1][5][2], data[1][5][3]) 
            
        #click
            for name, data in self.active_popups.items():
                if (data[0][2] and (event1 or data[0][10])):
                    data[0][10] = True
                    t = data[0][1] / (data[0][7] / 10)
                    t = max(0, min(t, 1))  
                    eased_t = out_circ(t)
                    new_width = lerp(data[0][4][0], data[0][4][0] * 1.1, eased_t)
                    new_height = lerp(data[0][4][1], data[0][4][1] * 1.1, eased_t)
                    data[0][0] = pygame.transform.smoothscale(data[0][6], (int(new_width), int(new_height)))
                    data[0][8] = data[0][0].get_rect().center
                    data[0][5] = pygame.Rect((data[0][0].get_rect()[0] - (data[0][8][0])) + data[0][9][0], (data[0][0].get_rect()[1] - (data[0][8][1])) + data[0][9][1], data[0][5][2], data[0][5][3]) 
                    if event2:
                        data[0][10] = False
                        event2 = False
                        event1 = False
                        data[0][2] = False
                        data[0][3]()
                else:
                    data[0][10] = False

                if (data[1][2] and (event1 or data[1][10])):
                    data[1][10] = True
                    t = data[1][1] / (data[1][7] / 10)
                    t = max(0, min(t, 1))  
                    eased_t = out_circ(t)
                    new_width = lerp(data[1][4][0], data[1][4][0] * 1.1, eased_t)
                    new_height = lerp(data[1][4][1], data[1][4][1] * 1.1, eased_t)
                    data[1][0] = pygame.transform.smoothscale(data[1][6], (int(new_width), int(new_height)))
                    data[1][8] = data[1][0].get_rect().center
                    data[1][5] = pygame.Rect((data[1][0].get_rect()[0] - (data[1][8][0])) + data[1][9][0], (data[1][0].get_rect()[1] - (data[1][8][1])) + data[1][9][1], data[1][5][2], data[1][5][3]) 
                    if event2:
                        data[1][10] = False
                        event2 = False
                        event1 = False
                        data[1][2] = False
                        data[1][3]()
                else:
                    data[1][10] = False
        

        #render
        for name, data in self.active_popups.items():
            self.surface.blit(data[2], data[2].get_rect())
            self.surface.blit(data[3], pygame.Rect(
                self.surface.get_width() // 2 - (data[3].get_rect()[2] // 2),
                self.surface.get_height() // 2 - (data[3].get_rect()[3] // 2),
                data[3].get_rect()[2],
                data[3].get_rect()[3]))
            self.surface.blit(data[4], pygame.Rect(
                self.surface.get_width() // 2 - (data[4].get_rect()[2] // 2),
                self.surface.get_height() // 2 - (data[4].get_rect()[3] // 2),
                data[4].get_rect()[2],
                data[4].get_rect()[3]))
            self.surface.blit(data[0][0].convert_alpha(), data[0][5])
            self.surface.blit(data[1][0].convert_alpha(), data[1][5])
        


screens = {
    "home": 0,
    "settings": 1
}

#animations
def out_circ(t):
    return np.sqrt(1 - (t - 1) ** 2)

def lerp(start, end, t):
  return (1 - t) * start + t * end
