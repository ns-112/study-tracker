import animations as anim
import pygame
import pyautogui
import os


src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = f'{project_dir}\\textures\\'

CENTER = (pyautogui.size().width // 2, pyautogui.size().height // 2)
WIDTH = 1280
HEIGHT = 720
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()

img = pygame.image.load(f"{textures_dir}stock.png")


elapsed_time = 0
dt = 0
running = True


image_object = anim.object(img, screen)
image_object.addAnimationTrack("scale", [[0, 1, 1], [0.5, 1.15, 1.15, "out_circ"], [1, 1, 1, "in_circ"]], loop = True)





while running:

    


    for event in pygame.event.get():
    
        
        if (event.type == pygame.QUIT):
            running = False
    image_object.updateObject(dt)

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    elapsed_time += dt


pygame.quit()