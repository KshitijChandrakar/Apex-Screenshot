
TotalPositions = 4
Positions = []
hotkeyShortcut = '<ctrl>+<shift>+z'
Filename = "test.md"



from PIL import ImageGrab
from pynput import keyboard, mouse
import time
import threading
from Filenames import *

#---------------------------------------------------------
# Initialize the controllers and the Keys
MouseCon = mouse.Controller()
keyboardController = keyboard.Controller()
Key = keyboard.Key

#---------------------------------------------------------
# This Gets us a List of 3 Positions
def getPositions():
    print("Move mouse to your position, and press", hotkeyShortcut)
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
    MouseCon.click(mouse.Button.left, 1)
    time.sleep(1)
    keyboardClick([Key.ctrl, 'a'])
    time.sleep(1)
    keyboardClick([Key.backspace,])
    time.sleep(1)
    keyboardController.type(Letters)
    time.sleep(2)

#---------------------------------------------------------
#Image Saver with filenames, i dont know why the Positioning wont work correctly
def GetImage():
    ssImg = ImageGrab.grab()
    # ssImg = ImageGrab.grab([min(Positions[1][0],Positions[2][0]), min(Positions[1][1],Positions[2][1]), max(Positions[1][0],Positions[2][0]), max(Positions[1][1],Positions[2][1])])
    filename = generateFilename("SS.jpg")
    ssImg.save(filename)
    return filename
    #str(int(time.time())) +
#---------------------------------------------------------
Commands = []
lineNos = []
def interpretMarkdown():
    global Commands
    global lineNos
    CurrentCommand = ""
    with open(Filename, 'r') as file:
        Found = False
        lines = file.readlines()
        for l in range(len(lines)):
            if not Found:
                lines[l] = lines[l].strip()
                if '```SQL' ==  lines[l].strip():
                    Found = True
                    #print("Found at", l + 1)
                    continue
            else:
                if '```' != lines[l].strip():
                    CurrentCommand += lines[l]
                    #print("Continued at", l+1, "|", lines[l], "|")
                else:
                    #print("Finshed at", l+1)
                    Found = False
                    Commands += [CurrentCommand,]
                    lineNos += [l + 1,]
                    CurrentCommand = ""
                    continue

#---------------------------------------------------------
def PressRun():
    MouseCon.position = Positions[3]
    MouseCon.click(mouse.Button.left,1)
#---------------------------------------------------------
def write_to_line(Filename, line_num, new_content):
    # Read the file content into a list
    with open(Filename, 'r') as file:
        lines = file.readlines()

    # Modify the desired line (note: line_num is 1-based, so subtract 1)
    if 0 <= line_num - 1 < len(lines):
        print(lines[line_num - 1], end = "")
        lines[line_num - 1] += new_content + "\n"
        print("++")
        print(lines[line_num - 1], end = "")
        print("--")
    else:
        print(f"Line {line_num} does not exist in the file.")
        return

    # Write the updated content back to the file
    with open(Filename, 'w') as file:
        file.writelines(lines)
#---------------------------------------------------------

interpretMarkdown()
print("-" * 10)
print("The Commands to Run Are:")
for i in Commands:
    print(i)
print("And Line Numbers are:", lineNos)
print("-" * 10)
print()
print("-" * 10)
getPositions()
print("-" * 10)
for i in range(len(Commands)):
    KeyType(Commands[i])
    filename = GetImage()
    write_to_line(Filename, lineNos[i], f"[!]({filename})")
