import pygame
import os
import pyautogui
from pygame._sdl2.video import Window
import guie
import timeline as tl
import cv2
import numpy as np
import setup
import threading

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
screen = pygame.display.set_mode((0, HEIGHT), flags=pygame.RESIZABLE | pygame.NOFRAME | pygame.SRCALPHA) 
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
current_page = 0

running = True
opening = False
closing = False
commit_close = False
commit_final_close = False

click_event = False
release_event = True

timeline = tl.timeline()
timeline.add_event(0.1, "start_open")
timeline.add_event(0.6, "end_open")
timeline.add_event(-1, "start_close") #set to -1 to unbind it
timeline.add_event(-1, "end_close") #set to -1 to unbind it


frame = None
frame_surface = None


def capture_frames():
    global frame_surface
    for frame in setup.eyeDetection():

        frame_surface = frame
 

#button callbacks
def b_close():
    if (home.active):
        home.active = False
        timeline.events["start_close"] = 0.2 + elapsed_time
        timeline.events["end_close"] = 0.7 + elapsed_time
        global commit_close
        commit_close = True

def b_test():
    print("popup")
    home.create_basic_popup(800, 400, None, b_change_page, button_1_name = "close", button_2_name = "page 2")

def b_generic():
    print("button clicked")

def b_change_page():
    print("clicked")
    global current_page
    current_page = 1

def b_start_demo():
    global current_page
    current_page = 2

#screens
home = guie.gui_screen(screen, 0)
settings = guie.gui_screen(screen, 1)
tracker = guie.gui_screen(screen, 2)


#buttons
home.create_button(b_close, "exit", x = 25, y = 25)
home.create_button(b_test, "stock", x = 400, y = 100)
home.create_button(b_start_demo, "tracking", x = (pyautogui.size().width // 2) - (WIDTH / 3), y = (pyautogui.size().height // 2) - (HEIGHT / 3))

settings.create_button(b_close, "exit", x = 25, y = 25)

tracker.create_button(b_close, "exit", x = 25, y = 25)



page_tracker = 0















while running:

    


    for event in pygame.event.get():
        if (event.type == pygame.MOUSEBUTTONDOWN and not click_event):
            click_event = True
            release_event = False
            break
        elif (event.type == pygame.MOUSEBUTTONUP):
            release_event = True
            click_event = False
            break
        
        if (event.type == pygame.QUIT):
            running = False
    
    home.update(dt, click_event, release_event, current_page)
    home.update_active_popups(dt, click_event, release_event)
    settings.update(dt, click_event, release_event, current_page)
    settings.update_active_popups(dt, click_event, release_event)

    tracker.update_active_popups(dt, click_event, release_event)

    if current_page == 2 and page_tracker == 0:
        page_tracker += 1
        thread = threading.Thread(target=capture_frames, daemon=True)
        thread.start()
   
    tracker.update(dt, click_event, release_event, current_page, frame_surface)
 
    
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000

    #opening and closing animation
    
    if (elapsed_time >= timeline.events["start_open"] and elapsed_time <= timeline.events["end_open"]):
        opening = True
        transition_time += dt
    elif (elapsed_time > timeline.events["end_open"] and not commit_close):
        opening = False
        transition_time = 0
    
    if (elapsed_time >= timeline.events["start_close"] and elapsed_time <= timeline.events["end_close"] and commit_close and release_event):
        
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
    
    if (elapsed_time > timeline.events["end_close"] + 1 and commit_close and release_event):
            print("closing failed due to unknown reason. forced close automatically.")
            running = False
    
    elapsed_time += dt
    

pygame.quit()
