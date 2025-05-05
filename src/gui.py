import pygame
import os
import pyautogui
from pygame._sdl2.video import Window
import guie
import timeline as tl
import cv2
import numpy as np
import detect
from detect import eyeDetection
import threading
import json
import animations as anim
import AfterStudyGUI
import time


WIDTH = 640
HEIGHT = 360
window_anims = False
BASE_POS = (pyautogui.size().width // 2 - (WIDTH / 2), (pyautogui.size().height // 2) - (HEIGHT / 2))

src_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(src_dir)
textures_dir = os.path.join(project_dir, 'textures')

pygame.init()
screen = pygame.display.set_mode((0, HEIGHT), flags=pygame.RESIZABLE | pygame.SRCALPHA) 
window = Window.from_display_module()
clock = pygame.time.Clock()

pygame.display.set_caption("Study Tracker")


    



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

stop = False
frame = None
frame_surface = None


ld_toggle = False
lwk_mode = False


tracker_time = 0


pause = False

totalTime = 0



def capture_frames():
    global frame_surface
    global distractedSeconds
    global totalTime
    global timeStamps
    global timeStampLen

    for frame,distractedSeconds,totalTime,timeStamps,timeStampLen in detect.eyeDetection():
        
        frame_surface = frame
        distractedSeconds = distractedSeconds
        totalTime = totalTime
        timeStampLen = timeStampLen
        timeStamps = timeStamps
        if(stop):
            
            break
    

#button callbacks
def b_close():
    if (home.active):
        home.active = False
        timeline.events["start_close"] = 0.2 + elapsed_time
        timeline.events["end_close"] = 0.7 + elapsed_time
        global commit_close
        commit_close = True

def b_graph():

    with open(os.path.join(project_dir, 'data', 'plot.json'), 'r') as file:
        python_dict = json.load(file)
    home.create_graph_popup(python_dict['y'])

def b_generic():
    print("button clicked")

def b_change_page():
    print("clicked")
    global current_page
    current_page = 1

def b_tracking():
    global current_page
    current_page = 2

def b_home():
    global totalTime
    if totalTime != 0:
        global current_page
        current_page = 0
        global stop
        stop = True
        global page_tracker
        page_tracker= 0
        global screen
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.SRCALPHA)
        window.position = (BASE_POS[0], BASE_POS[1]) 
        
        



def b_lockdown():
    global ld_toggle
    ld_toggle = not ld_toggle

def b_lwkmode():
    global lwk_mode
    lwk_mode = not lwk_mode




#screens
home = guie.gui_screen(screen, 0)
settings = guie.gui_screen(screen, 1)
tracker = guie.gui_screen(screen, 2)



#buttons
home.create_static_texture("bg")
home.create_button(b_close, "exit", (-(WIDTH / 2) + 35, (HEIGHT / 2) - 35))
home.create_button(b_graph, "graph", (-(WIDTH / 2) + 200, 0))
home.create_button(b_tracking, "tracking", (160, -70))

home.create_button(b_lockdown, "tick_empty", (80, 0), is_toggle = True, with_text = "lockdown mode")
home.create_button(b_lwkmode, "tick_empty", (80, 70), is_toggle = True, with_text = "hidden mode")

tracker.create_button(b_home, "exit", (-(WIDTH / 2) + 35, (HEIGHT / 2) - 35))
tracker.create_label("Study Session:", (0,  (HEIGHT / 2) - 20), does_change = True, data = tracker_time)



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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                if lwk_mode:
                    b_home()
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.SRCALPHA)
                    window.position = (BASE_POS[0], BASE_POS[1]) 

            elif event.key == pygame.K_SPACE:
                
                if os.path.exists("paused"):
                    f.close()
                    os.remove("paused")
                else:
                     f = open("paused", "w") 


    home.update(dt, click_event, release_event, current_page, toggle_states=[ld_toggle, lwk_mode])
    settings.update(dt, click_event, release_event, current_page)


    if current_page == 2 and page_tracker == 0:
        
        page_tracker += 1

        thread = threading.Thread(target=capture_frames, daemon=True)
        thread.start()
        if ld_toggle and not lwk_mode:
            del tracker.labels[0]
            screen = pygame.display.set_mode(pyautogui.size(), flags=pygame.RESIZABLE | pygame.SRCALPHA | pygame.NOFRAME) 
            window.position = (0, 0)
            tracker.create_label("Study Session:", (0,  (pyautogui.size().height / 2) - 20), does_change = True, data = tracker_time)
        elif lwk_mode and not ld_toggle:
            screen = pygame.display.set_mode((1, 1), flags=pygame.RESIZABLE | pygame.SRCALPHA | pygame.NOFRAME) 
            window.position = (0, 0)
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.SRCALPHA)
            window.position = (BASE_POS[0], BASE_POS[1]) 
       
    
    tracker.update(dt, click_event, release_event, current_page, frame_surface)
    tracker.labels[0].update_data(tracker_time)

    if current_page == 2 and totalTime != 0:
        if lwk_mode and page_tracker == 1:
            page_tracker += 1
            print("starting session")
        tracker_time += dt
    else:
        tracker_time = 0
    if pause == False:
        pygame.display.flip()

        
        dt = clock.tick(60) / 1000

    #opening and closing animation
    
    if (window_anims):
        pass
    else:
        opening = False
        if elapsed_time == 0:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.RESIZABLE | pygame.SRCALPHA) 
            window.position = (BASE_POS[0], BASE_POS[1])
        if commit_close and release_event:
            running = False
            closing = False
        
    

    
    if (elapsed_time > timeline.events["end_close"] + 1 and commit_close and release_event):
            print("closing failed due to unknown reason. forced close automatically.")
            running = False
    
    elapsed_time += dt
    
stop = True
if os.path.exists("paused"):
    os.remove("paused")
pygame.quit()

