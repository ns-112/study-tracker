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

    def create_button(self, callback, texture = "test_button", x = pyautogui.size().width // 2, y = pyautogui.size().height // 2, scale = 1, animation_length = 0.5):
        button = pygame.image.load(f'{textures_dir}{texture}.png')
        rect = button.get_rect()
        rect.topleft = (x, y)
        size = (pygame.Surface.get_width(button) * scale, pygame.Surface.get_height(button) * scale)
        self.buttons[texture] = [button, 0, False, callback, size, rect, button, animation_length]
    
    def update(self, dt, event):
        
        #render
        self.surface.fill((0, 0, 0))
        for name, data in self.buttons.items():
            self.surface.blit(data[0], data[0].get_rect())

        #hover
        for name, data in self.buttons.items():
            if data[5].collidepoint(pygame.mouse.get_pos()):
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

        #click
        for name, data in self.buttons.items():
            if event and data[2]:
                data[2] = False
                data[3]()


screens = {
    "home": 0,
    "settings": 1
}

#animations
def out_circ(t):
    return np.sqrt(1 - (t - 1) ** 2)

def lerp(start, end, t):
  return (1 - t) * start + t * end