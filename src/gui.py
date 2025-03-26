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


#lerp value
t = 0
#delta time
dt = 0
#total time
elapsed_time = 0
#self explanitory
transition_time = 0

running = True
opening = False
closing = False
commit_close = False
commit_final_close = False

click_event = False

timeline = tl.timeline()
timeline.add_event(0.1, "start_open")
timeline.add_event(0.6, "end_open")
timeline.add_event(-1, "start_close") #set to -1 to unbind it
timeline.add_event(-1, "end_close") #set to -1 to unbind it


#button callbacks
def b_close():
    timeline.events["start_close"] = 0.1 + elapsed_time
    timeline.events["end_close"] = 0.6 + elapsed_time
    global commit_close
    commit_close = True


#screens
home = ge.gui_screen(screen, 0)


#buttons
home.create_button(b_close, "exit", 0, 0)



















while running:
   



    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN):
            click_event = True
        else:
            click_event = False
        if (event.type == pygame.QUIT):
            running = False
    
    home.update(dt, click_event)



    
    
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

    #opening and closing animation
    
    if (elapsed_time >= timeline.events["start_open"] and elapsed_time <= timeline.events["end_open"]):
        opening = True
        transition_time += dt
    elif (elapsed_time > timeline.events["end_open"] and not commit_close):
        opening = False
        transition_time = 0
    
    if (elapsed_time >= timeline.events["start_close"] and elapsed_time <= timeline.events["end_close"] and commit_close):
        
        closing = True
        transition_time += dt
    elif(elapsed_time > timeline.events["end_close"] and timeline.events["start_close"] != -1):
        closing = False
        transition_time = 0
        
    

    if closing: 
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
