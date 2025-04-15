import animations as anim
import pygame
import pyautogui
import os


src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = f'{project_dir}\\textures\\'


WIDTH = 1280
HEIGHT = 720
CENTER = (WIDTH // 2, HEIGHT // 2)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()

img = pygame.image.load(f"{textures_dir}stock.png")


elapsed_time = 0
dt = 0
running = True


image_object = anim.object(img, screen, (20, 20))
image_object.addAnimationTrack("s", [[0, 1, 1], [.15, 1.05, 1.05, "out_circ"]])
#image_object.addAnimationTrack("p", [[0, 0, 0], [0.5, 200, 5, "in_out_sine"], [1, 0, 0, "in_out_sine"]], loop = True)





while running:

    


    for event in pygame.event.get():
    
        
        if (event.type == pygame.QUIT):
            running = False
    image_object.updateObject(dt)
    if image_object.object_rect.collidepoint(pygame.mouse.get_pos()):
        image_object.scale[0].argument1 = True
    else:
        image_object.scale[0].argument1 = False

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    elapsed_time += dt


pygame.quit()