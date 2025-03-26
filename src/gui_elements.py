import pygame
import os
import numpy as np


src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = f'{project_dir}\\textures\\'

screens = {
    "home": 0,
    "settings": 1
}

button_textures = {
    "exit": f'{textures_dir}exit.png'
}

exit = pygame.image.load(button_textures["exit"])


buttons = [
    exit
]

button_matches = {
    exit: "exit"
}


def close():
    print("Button clicked!")
    return True  


def draw_gui(screen, id="home"):
    screen.fill((0, 0, 0))
    id = screens[id]
    match id:
        case 0:
            pass
    for b in buttons:
        screen.blit(b, b.get_rect())
        b.get_rect().move(40, 40)


def on_hover(mouse, event, deltatime):
    for button in buttons:
        

        match button_matches[button]:
            
            case "exit":
                if check_button_clicked(button, close, mouse, event, deltatime):
                    return True  
    return False 


def check_button_clicked(button, callback, mouse, event, dt):
    if button.get_rect().collidepoint(mouse):  
        
        if event.type == pygame.MOUSEBUTTONDOWN:  
            return callback()  
    return False  





#animations
def ease_out_sine(t):
    return np.sin((t * np.pi) / 2)