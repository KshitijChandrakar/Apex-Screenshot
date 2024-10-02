
TotalPositions = 1
Positions = []
hotkeyShortcut = '<ctrl>+<shift>+z'




from PIL import ImageGrab
from pynput import keyboard, mouse
import time
import threading

#---------------------------------------------------------
# Initialize the controllers and the Keys
MouseCon = mouse.Controller()
keyboardController = keyboard.Controller()
Key = keyboard.Key

#---------------------------------------------------------
# This Gets us a List of 3 Positions
def getPositions():
    print("Mose mouse to your position, and press", hotkeyShortcut)
    def GetMousePos():
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
                time.sleep(0.1)
            else:
                print("Timed Out, Exiting Program...")
                listener.stop()
                listener.join(1)
                exit(2) # Exit on Timeout
    listener.join(2)

#---------------------------------------------------------
#This Goes to the selected location, selects everytthing, presses backspace and types whatever you pass to it
def KeyType(Letters):
    def keyboardClick(key):
        if type(key) == "<class 'str'>":
            keyboardController.press(key)
            keyboardController.release(key)
        else:
            for i in key:
                keyboardController.press(i)
            for i in key:
                keyboardController.release(i)
    MouseCon.position = Positions[0]
    time.sleep(0.1)
    MouseCon.click(mouse.Button.left, 1)
    time.sleep(0.1)
    keyboardClick([Key.ctrl, 'a'])
    time.sleep(0.1)
    keyboardClick([Key.backspace,])
    time.sleep(0.1)
    keyboardController.type(Letters)
#---------------------------------------------------------
getPositions()
KeyType("ACS")
