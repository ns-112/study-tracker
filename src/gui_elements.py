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

    def create_button(self, callback, texture = "test_button", x = pyautogui.size().width // 2, y = pyautogui.size().height // 2):
        button = pygame.image.load(f'{textures_dir}{texture}.png')
        rect = button.get_rect()
        rect.topleft = (x, y)
        self.buttons[texture] = [button, 0, False, callback]
    
    def update(self, dt, event):
        
        #render
        self.surface.fill((0, 0, 0))
        for name, data in self.buttons.items():
            self.surface.blit(data[0], data[0].get_rect())

        #hover
        for name, data in self.buttons.items():
            if data[0].get_rect().collidepoint(pygame.mouse.get_pos()):
                data[2] = True
            else:
                data[2] = False
            
        for name, data in self.buttons.items():
            if data[2]:
                if data[1] < 1:
                    data[1] += dt
            else:
                if data[1] > 0:
                    data[1] -= dt
        
        #click
        for name, data in self.buttons.items():
            if event and data[2]:
                data[3]()


screens = {
    "home": 0,
    "settings": 1
}

#animations
def ease_out_sine(t):
    return np.sin((t * np.pi) / 2)