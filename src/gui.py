import pygame
import os
import pyautogui
from pygame._sdl2.video import Window
import gui_elements as ge
import timeline as tl

# Outback easing
def ease_out_back(t, s=1.70158):
    t -= 1
    return (t * t * ((s + 1) * t + s) + 1)

# Back-in easing
def ease_in_back(t, s=1.70158):
    return t * t * ((s + 1) * t - s)

WIDTH = 1280
HEIGHT = 720
BASE_POS = (pyautogui.size().width // 2 - (WIDTH / 2), (pyautogui.size().height // 2) - (HEIGHT / 2))

src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)

pygame.init()
screen = pygame.display.set_mode((0, HEIGHT), flags=pygame.RESIZABLE | pygame.NOFRAME) 
window = Window.from_display_module()
clock = pygame.time.Clock()



elapsed_time = 0
transition_time = 0
running = True

timeline = tl.timeline()
timeline.add_event(0.1, "start_open")
timeline.add_event(0.6, "end_open")
timeline.add_event(-1, "start_close") #set to -1 to unbind it
timeline.add_event(-1, "end_close") #set to -1 to unbind it




opening = False
closing = False
commit_close = False
commit_final_close = False
#lerp value
t = 0
dt = 0


while running:
    loop_count = 0
    mouse = pygame.mouse.get_pos()
    ge.draw_gui(screen, "home")



    for event in pygame.event.get():
        
        if (loop_count == 0):
            
            commit_close = ge.on_hover(mouse, event, dt)
            
            if (commit_close == True): 
                
                timeline.events["start_close"] = 0.1 + elapsed_time
                timeline.events["end_close"] = 0.6 + elapsed_time
        if event.type == pygame.QUIT:
            running = False

        
        loop_count += 1
            
    if commit_close:
        commit_final_close = True


    
    
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

    #opening and closing animation
    
    if (elapsed_time >= timeline.events["start_open"] and elapsed_time <= timeline.events["end_open"]):
        opening = True
        transition_time += dt
    elif (elapsed_time > timeline.events["end_open"] and commit_final_close != True):
        opening = False
        transition_time = 0
    
    if (elapsed_time >= timeline.events["start_close"] and elapsed_time <= timeline.events["end_close"] and commit_final_close == True):
        
        closing = True
        transition_time += dt
    elif(elapsed_time > timeline.events["end_close"] and timeline.events["start_close"] != -1):
        closing = False
        transition_time = 0
        
    

    if closing:
        print(transition_time)  
        t = min(transition_time / (timeline.events["end_close"] - timeline.events["start_close"]), 1)
        x = int((1 - ease_in_back(t)) * WIDTH)
        if (abs(t + 0.03) >= 1): 
            x = 0
        window.size = (x + 1, HEIGHT)
        window.position = (pyautogui.size().width // 2 - (x / 2), BASE_POS[1])
        if (x == 0):
            running = False  

    if opening:
        t = min(transition_time / (timeline.events["end_open"] - timeline.events["start_open"]), 1)  
        x = int(ease_out_back(t) * WIDTH)
        window.size = (x, HEIGHT)
        window.position = (pyautogui.size().width // 2 - (x / 2), BASE_POS[1])
    
    elapsed_time += dt
    

pygame.quit()
