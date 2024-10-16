
from Filenames import *
import threading
import time
from pynput import keyboard, mouse
from PIL import ImageGrab
import ctypes
import os
TotalPositions = 4
Positions = []
hotkeyShortcut = '<ctrl>+<shift>+z'
Full_Path = "D:\My project\Apex Screenshot\test.md"
GlobalTimeout = 1000

# ---------------------------------------------------------

user32 = ctypes.windll.user32
dpi_scale = user32.GetDpiForWindow(user32.GetForegroundWindow()) / 96


# ---------------------------------------------------------
# Initialize the controllers and the Keys

MouseCon = mouse.Controller()
keyboardController = keyboard.Controller()
Key = keyboard.Key

# ---------------------------------------------------------


def Set_Path(path):
    global Path
    global Filename
    Path, Filename = os.path.split(path)

    try:
        os.chdir(Path)
    except FileNotFoundError as e:
        print(f"Error: {e}")

    pass
# ---------------------------------------------------------
# This Gets us a List of 3 Positions


def getPositions(N=GlobalTimeout):  # Number of secondns to timeout
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
    while True:
        if len(Positions) >= TotalPositions:
            listener.stop()
            break
        else:
            if n < N:
                n += 1
                time.sleep(0.1)
            else:
                print("Timed Out, Exiting Program...")
                listener.stop()
                listener.join(1)
                exit(2)  # Exit on Timeout
    listener.join(2)

# ---------------------------------------------------------
# This Goes to the selected location, selects everytthing, presses backspace and types whatever you pass to it


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

# ---------------------------------------------------------
# Image Saver with filenames, i dont know why the Positioning wont work correctly

# Get the scaling factor of the primary monitor
# print(dpi_scale)


def DefineBBox():
    global bbox
    bbox = [min(Positions[2][0], Positions[3][0]),
            min(Positions[2][1], Positions[3][1]),
            max(Positions[2][0], Positions[3][0]),
            max(Positions[2][1], Positions[3][1])]
    bbox = tuple(int(coordinate * dpi_scale) for coordinate in bbox)


def GetImage():
    # ssImg = ImageGrab.grab()
    # print(Positions[1] + Positions[2])

    # print(bbox)
    ssImg = ImageGrab.grab(bbox)
    filename = generateFilename("SS.jpg")
    ssImg.save(filename)
    return filename
    # str(int(time.time())) +


def ImageChanged(timeout=10):
    PrevImage = 0
    ssImg = ImageGrab.grab(bbox)
    changedAmt = 0
    time.sleep(1)
    for i in range(timeout - 1):
        time.sleep(0.5)
        PrevImage = ssImg.copy()
        ssImg = ImageGrab.grab(bbox)
        if PrevImage != ssImg:
            # print(f"changed at {i} seconds")
            if changedAmt >= 1:
                time.sleep(2)
                return True
            changedAmt += 1
    print(f"Timed Out While Getting the Results, at {timeout} seconds")
    return False
    # str(int(time.time())) +


# ---------------------------------------------------------
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
                if '```SQL' == lines[l].strip():
                    Found = True
                    # print("Found at", l + 1)
                    continue
            else:
                if '```' != lines[l].strip():
                    CurrentCommand += lines[l]
                    # print("Continued at", l+1, "|", lines[l], "|")
                else:
                    # print("Finshed at", l+1)
                    Found = False
                    Commands += [CurrentCommand,]
                    lineNos += [l + 1,]
                    CurrentCommand = ""
                    continue

# ---------------------------------------------------------


def PressRun():
    MouseCon.position = Positions[1]
    MouseCon.click(mouse.Button.left, 1)
# ---------------------------------------------------------


def write_to_line(Filename, line_num, new_content):
    # Read the file content into a list
    with open(Filename, 'r') as file:
        lines = file.readlines()
        print(lines)
    # Modify the desired line (note: line_num is 1-based, so subtract 1)
    if 0 <= line_num - 1 < len(lines):
        # print(lines[line_num - 1], end = "")
        lines[line_num - 1] += new_content + "\n"
        # print("++")
        # print(lines[line_num - 1], end = "")
        # print("--")
    else:
        print(f"Line {line_num} does not exist in the file.")
        return

    # Write the updated content back to the file
    with open(Filename, 'w') as file:
        file.writelines(lines)


# ---------------------------------------------------------
# def CollectCommands():
Path, Filename =
interpretMarkdown()
print("-" * 10)
print("The Commands to Run Are:")
for i in Commands:
    print(i)
print("And Line Numbers are:", lineNos)
print("-" * 10)
# def CollectPositions():
print("-" * 10)
getPositions()
print("-" * 10)
print("-" * 10)
DefineBBox()
print("Screenshot Box is:", bbox)
print("-" * 10)
# def RunCommands():
for i in range(len(Commands)):
    KeyType(Commands[i])
    time.sleep(1)
    PressRun()
    if ImageChanged():
        filename = GetImage()
        write_to_line(Filename, lineNos[i] + i, f"![[{filename}]]")
time.sleep(3)
KeyType("DONE!!!")
