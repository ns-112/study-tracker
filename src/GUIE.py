import pygame
import os
import numpy as np
import pyautogui


src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = f'{project_dir}\\textures\\'

class gui_screen:
    def __init__(self, screen, page = 0):
        self.page = page
        self.buttons = {}
        self.surface = screen

    def create_button(
            self, 
            #base attributes
            callback,                   #----method----
            texture = "test_button",    #----string----
            #layout options
            x = 0,                      #----int-------
            y = 0,                      #----int-------
            column = 0,                 #----int-------
            anchor = pygame.Rect.center,#----rect type-
            row = 0,                    #----int-------
            #animation/extra
            scale = 1,                  #----float-----
            animation_length = 0.5      #----float-----
            ):
        
        button = pygame.image.load(f'{textures_dir}{texture}.png')
        size = (pygame.Surface.get_width(button) * scale, pygame.Surface.get_height(button) * scale)
        rect = button.get_rect()
        rect.width = size[0]
        rect.height = size[1]
        if x <= size[0]:
            x = size[0]
        if y <= size[1]:
            y = size[1]
        rect = pygame.Rect(abs(x), abs(y), size[0], size[1])
        original_pos = (x, y)
       
        scaled_rect = pygame.Rect(rect[2], rect[3], size[0], size[1])

        self.buttons[texture] = [
            button, #base button,                   0----pygame surface
            0, #lerp value,                         1----float
            False, #is hovering,                    2----boolean
            callback, #button callback,             3----method
            size, #scale modifier,                  4----tuple
            rect, #hover rect,                      5----pygame rect        
            button, #scalable coopy of texture,     6----pygame surface
            animation_length, #animation duration,  7----float
            scaled_rect, #scaled rect               8----pygame rect -> tuple 
            original_pos #original pos              9----tuple
            ]
        

    def create_popup(self, width, height, button_1_callback, button_2_callback, button_1 = "okay", button_2 = "cancel", x = pyautogui.size().width // 2, y = pyautogui.size().height // 2):
        pass


    
    def update(self, dt, event1, event2):
        
       

        #hover
        for name, data in self.buttons.items():
            if pygame.Rect(data[9][0] - (data[6].get_rect()[2] //2), data[9][1] - (data[6].get_rect()[3] // 2), data[4][0], data[4][1]).collidepoint(pygame.mouse.get_pos()):
                data[2] = True
            else:
                data[2] = False
            
        for name, data in self.buttons.items():
            if data[2]:
                if data[1] < (data[7] / 10):
                    
                    data[1] += dt
            else:
                if data[1] > 0:
                    data[1] -= dt
        

        #hover scale
        for name, data in self.buttons.items():
            t = data[1] / (data[7] / 10)
            t = max(0, min(t, 1))  
            eased_t = out_circ(t)
            new_width = lerp(data[4][0], data[4][0] * 1.25, eased_t)
            new_height = lerp(data[4][1], data[4][1] * 1.25, eased_t)
            data[0] = pygame.transform.smoothscale(data[6], (int(new_width), int(new_height)))
            data[8] = data[0].get_rect().center
            data[5] = pygame.Rect((data[0].get_rect()[0] - (data[8][0])) + data[9][0], (data[0].get_rect()[1] - (data[8][1])) + data[9][1], data[5][2], data[5][3]) 
            
            

        #click
        for name, data in self.buttons.items():
            if event1 and data[2] and not event2:
                event2 = True
                data[2] = False
                data[3]()


                t = data[1] / (data[7] / 10)
                t = max(0, min(t, 1))  
                eased_t = out_circ(t)
                new_width = lerp(data[4][0], data[4][0] * 1.1, eased_t)
                new_height = lerp(data[4][1], data[4][1] * 1.1, eased_t)
                data[0] = pygame.transform.smoothscale(data[6], (int(new_width), int(new_height)))
                data[8] = data[0].get_rect().center
                data[5] = pygame.Rect((data[0].get_rect()[0] - (data[8][0])) + data[9][0], (data[0].get_rect()[1] - (data[8][1])) + data[9][1], data[5][2], data[5][3]) 



        #render
        self.surface.fill((0, 0, 0))
        for name, data in self.buttons.items():
            
            self.surface.blit(data[0], data[5])
            


screens = {
    "home": 0,
    "settings": 1
}

#animations
def out_circ(t):
    return np.sqrt(1 - (t - 1) ** 2)

def lerp(start, end, t):
  return (1 - t) * start + t * end