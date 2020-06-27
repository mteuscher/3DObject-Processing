import sys
from tkinter import *
from tkinter import ttk, filedialog

def quitProgramm():
    sys.exit()

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

def run_object_extraction():
    pass









# GUI Arrangement
root = Tk()
root.title("Extract similar Objects from 3DOC counter output - MT Version")

folder_path = StringVar()

lbl1 = Label(master=root,textvariable=folder_path)
lbl1.grid(row=0, column=1)
button1 = Button(text="Browse", command=browse_button)
button1.grid(row=0, column=3)

lbl2 = Label(text=(
    "\nSelect a folder containing the ouput files of the 3D Objects counter plugin - MT version\n"
    "Make sure the correct folder was recognized\n" 
    "Have fun\n"
    ))
lbl2.grid(row=2, column=2)

button2 = Button(text="Start Processing", command=run_object_extraction)
button2.grid(row=3, column=2)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit", command=quitProgramm)

menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
root.mainloop()