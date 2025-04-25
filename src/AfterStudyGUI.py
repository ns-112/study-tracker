import numpy as np
import cv2
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from functools import reduce
from functools import partial
import math

from datetime import datetime


root = tk.Tk()
frame = tk.Frame(root)
left_frame = tk.Frame(frame, width = 500, height=600) 
right_frame = tk.Frame(frame, width = 500, height=600) 
study_label = tk.Label(right_frame, text="What did you study?", font=("Arial", 14))
study_entry = tk.Entry(right_frame, width=50, font=("Arial", 12))
confirmation_label = tk.Label(right_frame, text="", font=("Arial", 10))
log_text = tk.Text(right_frame, height=10, width=60, font=("Courier New", 10), wrap="word")

def log_study(timeStamps,totTime):
    topic = study_entry.get()
    distractions = len(timeStamps)
    if ((totTime / 60) > 1):
        totTime = f"{math.floor(totTime/60)}m {totTime - (math.floor(totTime/60) * 60)}s" 
    else: 
        totTime = f"{totTime}s"
    
    if topic.strip():
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - Distractions:{distractions} - {topic} - Time:{totTime} \n"
        with open("study_log.txt", "a") as f:
            f.write(log_entry)
        study_entry.delete(0, tk.END)
        confirmation_label.config(text=f"Logged: {topic}", fg="green")
        update_log_display()
    else:
        confirmation_label.config(text="Please enter a topic first.", fg="red")

def update_log_display():
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

def Graph(disTime,totTime,stamps,stamplen):
    update_log_display()
    focusedPer=(((totTime-disTime)/totTime) * 100)
    disPer = (disTime / totTime) * 100

    log_button = tk.Button(right_frame, text="Log Study Session", command=partial(log_study, stamplen, round(totTime)))
    
    root.title ("Study Tracker")
    root.geometry("1000x600")
    
    frame.pack(fill=tk.BOTH, expand = True)
    
    left_frame.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)
    
    right_frame.pack(side=tk.RIGHT, fill = tk.BOTH, expand = True)
    
    study_label.pack(pady=(20, 5))

    study_entry.pack(pady=5)

    confirmation_label.pack(pady=(5, 10))
    #PI CHART LABELS, SIZES,  AND COLORS.
    # sizes must equal to 100 
    labels = ['Study', 'Distracted']
    sizes = [focusedPer, disPer]  
    colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
    time_label = [ f"{x}, Period:{stamps[x]}s, Duration:{stamplen[x]}s" for x in stamps]
    time_label = reduce(combine, time_label)
    time_label = tk.Label(root, text = f"Timestamps:\n {time_label}")
    time_label.pack(pady=100)
    
    fig, ax = plt.subplots(figsize=(5, 3))  #Adjust size of the pie chart
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    ax.axis('equal') #makes sure our pi chart is a circle according to aspect ratio
    
    
    label = tk.Label(right_frame, text="Study Recommendations")
    label.pack(pady=50)
    
    top_label = tk.Label(root, text = "Study Overview")
    top_label.pack(side=tk.TOP, pady=20)
    log_button.pack(pady=(0, 10))

    log_display_label = tk.Label(right_frame, text="Logged Sessions:", font=("Arial", 14, "bold"))
    log_display_label.pack(pady=(10, 5))

    log_text.pack(pady=5)
    
    canvas = FigureCanvasTkAgg(fig, master=left_frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    root.mainloop()





