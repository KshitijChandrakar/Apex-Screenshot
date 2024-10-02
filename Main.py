
TotalPositions = 3
Positions = []
hotkeyShortcut = '<ctrl>+<shift>+z'




from PIL import ImageGrab
from pynput import keyboard, mouse
import time
import threading



#---------------------------------------------------------
# This Gets us a List of 3 Positions
def getPositions():
    def GetMousePos():
        MouseCon = mouse.Controller()
        pos = MouseCon.position
        print(pos, "Postion", len(Positions), "Selected")
        if len(Positions) < TotalPositions:
            Positions.append(pos)
            return True
        return False
    # Collect events until released
    listener = keyboard.GlobalHotKeys({
            hotkeyShortcut: GetMousePos
            })
    listener.start()
    n = 0
    N = 120 # Number of Seconds to Timeout
    while True:
        if len(Positions) >= TotalPositions:
            listener.stop()
            break
        else:
            if n < N:
                n+=1
                time.sleep(1)
            else:
                print("Timed Out, Exiting Program...")
                listener.stop()
                listener.join(1)
                exit(2) # Exit on Timeout
    listener.join(2)
#---------------------------------------------------------
