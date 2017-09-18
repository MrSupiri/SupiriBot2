import cv2
import pandas as pd
from motor import *
from random import randint
from optimizer import solveMaze
import os
import pickle
# import socket

fwd(0.7)

if os.path.isfile('/home/pi/SupiriBot/movements/movements.dat'):
    optimizedRun = True
    movements = pickle.load(open("/home/pi/SupiriBot/movements/movements.dat", "rb"))
    path = solveMaze(movements)
    print(path)
else:
    optimizedRun = False

# HOST = '192.168.1.100'
# PORT = 5000
# conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# conn.connect((HOST, PORT))

# noinspection PyArgumentList
cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
turns = 0
moves = []
lastMove = ''


def findError(lineState):
    """
    Get the LineState and generate a error Value
    line array        error
    0 0 0 0 1	        4
    0 0 0 1 1	        3
    0 0 0 1 0	        2
    0 0 1 1 0	        1
    0 0 1 0 0	        0
    0 1 1 1 0	        0
    0 1 1 0 0	        -1
    0 1 0 0 0	        -2
    1 1 0 0 0	        -3
    1 0 0 0 0	        -4

    LF = LineFollow
    RT = RightTurn
    LT = LeftTurn
    NL = NoLine
    TJ = T-Junction
    UK = UnKnown
    :param lineState:
    :return error,state:
    """
    state = 'LF'
    err = 0

    if lineState == [0, 0, 0, 0, 1]:
        err = 4
        state = 'LF'
    elif lineState == [0, 0, 0, 1, 1]:
        err = 3
        state = 'LF'
    elif lineState == [0, 0, 0, 1, 0]:
        err = 2
        state = 'LF'
    elif lineState == [0, 0, 1, 1, 0]:
        err = 1
        state = 'LF'
    elif lineState == [0, 0, 1, 0, 0]:
        err = 0
        state = 'LF'
    elif lineState == [0, 0, 1, 0, 0]:
        err = 0
        state = 'LF'
    elif lineState == [0, 1, 1, 0, 0]:
        err = -1
        state = 'LF'
    elif lineState == [0, 1, 0, 0, 0]:
        err = -2
        state = 'LF'
    elif lineState == [1, 1, 0, 0, 0]:
        err = -3
        state = 'LF'
    elif lineState == [1, 0, 0, 0, 0]:
        err = -4
        state = 'LF'
    elif lineState == [0, 0, 1, 1, 1]:
        err = 0
        state = 'RT'
    elif lineState == [0, 1, 1, 1, 1]:
        err = 0
        state = 'RT'
    elif lineState == [1, 1, 1, 0, 0]:
        err = 0
        state = 'LT'
    elif lineState == [1, 1, 1, 1, 0]:
        err = 0
        state = 'LT'
    elif lineState == [0, 0, 0, 0, 0]:
        err = 0
        state = 'NL'
    elif lineState == [1, 1, 1, 1, 1]:
        err = 0
        state = 'TJ'
    elif lineState == [1, 1, 0, 1, 1]:
        err = 0
        state = 'END'

    # elif lineState == [0, 1, 0, 1, 1]:
    #     err = 0
    #     state = 'END'
    # elif lineState == [1, 1, 0, 1, 0]:
    #     err = 0
    #     state = 'END'
    # elif lineState == [0, 1, 0, 1, 0]:
    #     err = 0
    #     state = 'END'

    return err, state


def fixCam(state):
    for _ in range(0, 9):
        _, _ = processImage()
    lineState, _ = processImage()
    _, currentState = findError(lineState[:5])
    if optimizedRun:
        currentState = path[turns]
    if state == currentState:
        return True
    else:
        return False


def fix90():
    """
    Weird Error - When Robot Turn 90 degree Camara is sees weird lines
    So with this Code We are just skipping 10 Frames we received then everyone is Happy ^_^
    :return:
    """
    stay()
    back(0.32)
    for _ in range(0, 12):
        _, _ = processImage()


def calculateTurn(lineState):
    """
    Get the lineState from processImage Function and find where is the robot at with findError
    Then Calculate Turn the Robot should Use
    :param lineState:
    :return:
    """
    global turns
    err, state = findError(lineState[:5])

    if optimizedRun and state != 'LF':
        try:
            state = path[turns]
        except:
            fwd(0.6)
            if os.path.isfile('/home/pi/SupiriBot/movements/movements.dat'):
                os.remove('/home/pi/SupiriBot/movements/movements.dat')
            time.sleep(900)

    if state == 'NL':
        if fixCam(state):
            turns += 1
            fwd(0.6)
            turn()
            moves.append('NL')
            fix90()
        else:
            lineFollower()
    elif state == 'RT':
        if fixCam(state):
            turns += 1
            if not optimizedRun:
                if not lineState[5]:
                    fwd(0.6)
                    right90()
                    moves.append('RT')
                    fix90()
                else:
                    fwd(0.2)
                    moves.append('FW')
            else:
                fwd(0.6)
                right90()
                moves.append('RT')
                fix90()
        else:
            lineFollower()
    elif state == 'LT':
        if fixCam(state):
            turns += 1
            fwd(0.6)
            left90()
            moves.append('LT')
            fix90()
        else:
            lineFollower()
    elif state == 'TJ':
        if fixCam(state):
            turns += 1
            fwd(0.6)
            left90()
            moves.append('LT')
            fix90()
        else:
            lineFollower()
    elif state == "FW":
        turns += 1
        fwd(0.4)
        for _ in range(0, 6):
            _, _ = processImage()
    elif state == "END":
        fwd(0.6)
        pickle.dump(moves, open("/home/pi/SupiriBot/movements/movements.dat", "wb"))
        time.sleep(900)
    else:
        fixError(err)

    return err


def fixError(err):
    """
    If Robot is in a Normal situation (not in 90 turn or something)
    Fix the Previously Generated Errors and Remember the movement made for future use
    :param err:
    :return:
    """
    global lastMove
    if err == 0:
        lastMove = 'F'
        fwd()
    elif err < 0:
        lastMove = 'L'
        while err != 0:
            left()
            err += 1
    else:
        lastMove = 'R'
        while err != 0:
            right()
            err -= 1


def randomMove():
    """
    What happen if Robot Stuck in a Situation Robot has no Idea what to do ?
    Easy Pry for RNG gods and do what the god says and hope for the best :D
    :return:
    """
    rm = randint(0, 2)
    if rm == 0:
        fwd()
    elif rm == 1:
        right()
    else:
        left()


def processImage():
    """
    Get the the Image from the WebCam and Convert it to GrayScale
    Then Convent it to a Binary Image to make Processing Easier
    Then Crop the Image and extract a 20x120 Image from the Middle of the Frame
    Then Find where is the Most Black Pixels are and enter those Value to line array as 0 or 1 ( 1 = Black, 0 = White )
    :return line,time_took:
    """
    last_time = time.time()
    lineState = [0, 0, 0, 0, 0, 0]
    frontLine = []
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # data = pickle.dumps(frame)
    # conn.send(data)
    _, img = cv2.threshold(frame[30:110, 0:160], 80, 255, cv2.THRESH_BINARY)
    for k in range(0, 5):
        box = img[55:80, k * 32:k * 32 + 32]
        df = pd.DataFrame(box)
        state = df[22].value_counts().idxmax()
        if state == 0:
            lineState[k] = 1
    for l in range(1, 4):
        box = img[20:50, l * 32:l * 32 + 32]
        df = pd.DataFrame(box)
        state = df[22].value_counts().idxmax()
        frontLine.append(state)
    if 0 in frontLine:
        lineState[5] = 1

    print(lineState)
    return lineState, last_time


def lineFollower():
    """
    Main Loop - Find where is the line and calculate the turn
    :return:
    """
    lineState, last_time = processImage()
    err = calculateTurn(lineState)
    #print('Loop Took:', round(time.time() - last_time, 3), 'LS:-', lineState, 'Error:', err, 'Last Move:', lastMove)


try:
    for i in range(0, 10):
        line, _ = processImage()
    print('optimizedRun', optimizedRun)
    time.sleep(1)
    while True:
        lineFollower()

except KeyboardInterrupt:
    print(moves)
    stay()
    cap.release()
