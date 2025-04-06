import numpy as np
import cv2
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


#GUI

root = tk.Tk()

root.title ("Study Tracker")
root.geometry("1000x600")

frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand = True)

left_frame = tk.Frame(frame, width = 500, height=600) 
left_frame.pack(side=tk.LEFT, fill = tk.BOTH, expand = True)

right_frame = tk.Frame(frame, width = 500, height=600) 
right_frame.pack(side=tk.RIGHT, fill = tk.BOTH, expand = True)

#PI CHART LABELS, SIZES,  AND COLORS.
# sizes must equal to 100 
labels = ['Study', 'Wandering', 'Distracted', 'Other']
sizes = [50, 30, 15, 5]  
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

fig, ax = plt.subplots(figsize=(5, 3))  #Adjust size of the pie chart
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
ax.axis('equal') #makes sure our pi chart is a circle according to aspect ratio

canvas = FigureCanvasTkAgg(fig, master=left_frame)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

label = tk.Label(right_frame, text="Study Recommendations")
label.pack(pady=50)

top_label = tk.Label(root, text = "Study Overview")
top_label.pack(side=tk.TOP, pady=20)


root.mainloop()
