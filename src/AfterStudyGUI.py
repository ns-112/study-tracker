import numpy as np
import cv2
import tkinter as tk #for our gui
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functools import reduce
from functools import partial
import math
import json
from datetime import datetime #for timestamping our log entries


root = tk.Tk()
frame = tk.Frame(root) #initializes our tkinter window

left_frame = tk.Frame(frame, width = 500, height=600) 
right_frame = tk.Frame(frame, width = 500, height=600) #splits our main window into two for our chart and user interface

study_label = tk.Label(right_frame, text="What did you study?", font=("Arial", 14))
study_entry = tk.Entry(right_frame, width=50, font=("Arial", 12))
confirmation_label = tk.Label(right_frame, text="", font=("Arial", 10))
log_text = tk.Text(right_frame, height=10, width=60, font=("Courier New", 10), wrap="word") #widgets for study input and logging studies

def get_study_recommendation(focus_percent, distractions): #Messages for the recommendations based off how focused/unfocused the user was
    if focus_percent > 90:
        return "Great job! You stayed super focused."
    elif focus_percent > 70:
        return "Good session, but try to reduce distractions next time."
    elif focus_percent > 50:
        return "You got some good work done, but consider different studying techniques"
    else:
        return "Try shorter sessions with breaks, or put your phone away to stay on track."
    
def log_study(timeStamps,totTime): #function that logs our study session to a text file
    topic = study_entry.get()
    distractions = len(timeStamps)
    if ((totTime / 60) > 1): #turns our total time into minutes and seconds
        totTime = f"{math.floor(totTime/60)}m {totTime - (math.floor(totTime/60) * 60)}s" 
    else: 
        totTime = f"{totTime}s"
    
    if topic.strip():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - Distractions:{distractions} - {topic} - Time:{totTime} \n" #Timestamps the users log entry also shows distractions, topic, and time
        with open("study_log.txt", "a") as f: #writes the log entry to a file
            f.write(log_entry)
        study_entry.delete(0, tk.END)
        confirmation_label.config(text=f"Logged: {topic}", fg="green")
        update_log_display()
    else:
        confirmation_label.config(text="Please enter a topic first.", fg="red") #Ensures the user enter a messsage before logging

def update_log_display(): #Displays the last few logs in the GUI
    try:
        with open("study_log.txt", "r") as f:
            lines = f.readlines()
        last_entries = lines[-5:] if len(lines) > 5 else lines
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, ''.join(last_entries))
    except FileNotFoundError:
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "No sessions logged yet.")

#GUI
def combine(x,y):
    return x + "\n" + y

def Graph(disTime,totTime,stamps,stamplen): #Main functions to build GUI and Graph
    
    focusedPer=(((totTime-disTime)/totTime) * 100) #Calculates the percentaged of focused and distracted time
    disPer = (disTime / totTime) * 100

    log_button = tk.Button(right_frame, text="Log Study Session", command=partial(log_study, stamplen, round(totTime))) #creates the button to log the session
    
    root.title ("Study Tracker") #our window title and size
    #root.state('zoomed')
    root.geometry("1000x600")

    top_label = tk.Label(root, text = "Study Overview") #top banner
    top_label.pack(side=tk.TOP, pady=(10,5))

    frame.pack(fill=tk.BOTH, expand = True) #layout setup
    left_frame.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)
    right_frame.pack(side=tk.RIGHT, fill = tk.BOTH, expand = True)

    label = tk.Label(right_frame, text="Study Recommendations") #recommendation section
    label.pack(pady=50)
    recommendation = get_study_recommendation(focusedPer, len(stamplen))
    rec_label = tk.Label(right_frame, text=recommendation, font=("Arial", 12), fg="blue", wraplength=400, justify="left")
    rec_label.pack(pady=(5, 20))

    study_label.pack(pady=(20, 5))

    study_entry.pack(pady=5)

    confirmation_label.pack(pady=(5, 10))
    #PI CHART LABELS, SIZES,  AND COLORS.
    # sizes must equal to 100 
    labels = ['Study', 'Distracted']
    sizes = [focusedPer, disPer]  
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    # Create the timestamp label text
    time_label_list = [f"{x}, Period: {stamps[x]}s, Duration: {stamplen[x]}s" for x in stamps]

    if time_label_list:
        time_label_text = reduce(combine, time_label_list)
    else:
        time_label_text = "No distractions recorded."

    
    fig, ax = plt.subplots(figsize=(5, 3))  #Adjust size of the pie chart
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal') #makes sure our pi chart is a circle according to aspect ratio

    #displays the rest of the GUI
    log_button.pack(pady=(0, 10))

    log_display_label = tk.Label(right_frame, text="Logged Sessions:", font=("Arial", 14, "bold"))
    log_display_label.pack(pady=(10, 5))

    log_text.pack(pady=5)
    update_log_display()

    #Embeds the pi chart into the left fram
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    #Show distraction timestamps
    time_label = tk.Label(right_frame, text=f"Timestamps:\n{time_label_text}", justify="left", anchor="w", font=("Courier New", 10), wraplength=400)
    time_heading = tk.Label(right_frame, text="Distraction Timestamps:", font=("Arial", 12, "bold"))
    time_heading.pack(pady=(10, 5))
    time_label.pack(pady=(10,20))

    root.mainloop()





