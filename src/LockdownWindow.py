import tkinter as tk
import tkinter.messagebox as msgbox

def on_closing(event=None):
    if msgbox.askokcancel("Quit", "Do you really want to end your study session?"):
        root.destroy()

root = tk.Tk()
root.title("Lockdown Window")


root.attributes("-fullscreen", True)
root.resizable(False, False)


root.bind("<q>", on_closing)

root.protocol("WM_DELETE_WINDOW", on_closing)

label = tk.Label(root, text="This study session is locked down.", font=("Arial", 24))
label.pack(pady=50)

root.mainloop()
