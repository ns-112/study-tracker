import animations as anim
import pygame
import pyautogui
import os
import json


src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = f'{project_dir}\\textures\\'


WIDTH = 1280
HEIGHT = 720
CENTER = (WIDTH // 2, HEIGHT // 2)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE)
clock = pygame.time.Clock()




elapsed_time = 0
dt = 0
running = True


with open(f'{project_dir}\\data\\plot.json', 'r') as file:
    python_dict = json.load(file)

y_values = python_dict['y']
print(y_values)

plot_is_active = False
plot = []
index = 0
for y in y_values:

    dot = anim.object(pygame.image.load(f"{textures_dir}dot.png"), screen, ((((400 // len(y_values)) * index) - 200), -100), False)
    dot.addAnimationTrack("p", [[0, 0, 0], [0.5, 0, 0], [1.5, 0, (y * 2), "in_out_sine"]])
    index += 1
    plot.append(dot)
    




image_object = anim.object(pygame.image.load(f"{textures_dir}stock.png"), screen, (20, 20), True)
#image_object.addAnimationTrack("s", [[0, 1, 1], [.15, 3, 3, "out_circ"]])
#image_object.addAnimationTrack("p", [[0, 0, 0], [0.5, 200, 5, "in_out_sine"], [1, 0, 0, "in_out_sine"]], loop = True)





while running:

    

    screen.fill((110, 110, 110))
    for event in pygame.event.get():
    
        
        if (event.type == pygame.QUIT):
            running = False
    image_object.updateObject(dt, 0)
    index = 0
    if plot_is_active:
        for point in plot:
            point.updateObject(dt, 0)
            if index < len(plot) - 1:
                pygame.draw.line(screen, (255, 255, 255), (point.attributes[0][0] + (point.object_rect[2] // 2), point.attributes[0][1] + (point.object_rect[3] // 2)), (plot[index + 1].attributes[0][0] + (plot[index + 1].object_rect[2] // 2), plot[index + 1].attributes[0][1] + (plot[index + 1].object_rect[3] // 2)))
            index += 1
    if elapsed_time > 2:
        plot_is_active = True

    pygame.display.flip()
    dt = clock.tick(60) / 1000
    elapsed_time += dt


pygame.quit()