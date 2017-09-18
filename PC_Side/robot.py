import time
import cv2
import numpy as np
import pandas as pd
from motor import *

def lineFollow(lineState):
	error = 0
	errorValues = [-2,-1,0,1,2]
	for i,state in enumerate(lineState[1:5]):
		if state:
			error = errorValues[i]
	if error == 0:
		fwd()
	elif error == -1:
		left()
	elif error == -2:
		left2()
	elif error == 1:
		right()
	elif error == 2:
		right2()

def doMagicalThings(l):
	if l[0]:
		left90()
	elif l[6]:
		right90()
	elif l == [0, 0, 0, 0, 0, 0, 0]:
		turn()

def processImage(originalIMG):
	_, img = cv2.threshold(originalIMG, 127, 255, cv2.THRESH_BINARY)

	line = [0, 0, 0, 0, 0, 0, 0]
	for i in range(0,7):
		box = img[70:100, 3+(i*22):3+(i*22+22)]
		df = pd.DataFrame(box)
		state = df[1].value_counts().idxmax()
		print(state)
		if state == 0:
			line[i] = 1
	img = img[70:100, 0:160]

	return line,img


def mainloop():
	cap = cv2.VideoCapture(0)
	cap.set(3, 160)
	cap.set(4, 120)
	while 1:
		_, frame = cap.read()
		originalImage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		lineState,processedIMG = processImage(originalImage)
		if lineState.count(1) <= 2 and not lineState.count(1) == 0:
			lineFollow(lineState)
		else:
			doMagicalThings(lineState)
		#print(lineState)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break



mainloop()
