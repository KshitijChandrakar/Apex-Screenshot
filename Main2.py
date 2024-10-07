from Main import *
from tkinter import *
Window = Tk()
Window.title("APEX SCREENSHOTTER")
Window.title("400x400")
Window.wm_attributes("-topmost", True)
Window.resizable(0,0)
Apex_Screenshotter_Text = Label(Window, text= 'APEX SCREENSHOTTER')
Collect_Positions = Button(Window, text='Start Recording', width=25, command=CollectPositions)
Collect_Commands = Button(Window, text='Collect Commands', width=20, command=CollectCommands)
Collect_Commands1 = Button(Window, text='Collect Commands', width=5, command=CollectCommands)

Run_Commands = Button(Window, text='Run Commands', width=25, command=RunCommands)
def SelectFile():
    global SelectedFile
    SelectedFile = filedialog.askopenfilename()
    Set_Path(SelectedFile)

Apex_Screenshotter_Text.grid(row = 0, column = 0, sticky = W, pady = 10)
Collect_Positions.grid(row = 1, column = 0, sticky = W, pady = 10)
Collect_Commands.grid(row = 2, column = 0, sticky = W, pady = 5)
Collect_Commands1.grid(row = 2, column = 1, sticky = W, pady = 5)
Run_Commands.grid(row = 3, column = 0, sticky = W, pady = 10)
Window.mainloop()
