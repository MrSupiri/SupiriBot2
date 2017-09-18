import cv2
import pandas as pd
from collections import Counter
import time

def findMode(df):
    state = []
    for i in range(0, 28,4):
        state.append(df[i].value_counts().idxmax())
    cmm = Counter(state).most_common()[0][0]
    return cmm
def processImage(originalIMG):
    _, img = cv2.threshold(originalIMG[30:110, 0:160], 100, 255, cv2.THRESH_BINARY)
    line = [0, 0, 0, 0, 0, 0]
    frontLine = []
    originalIMG = originalIMG[30:110, 0:160]
    for i in range(0, 5):
        box = img[60:70, i * 32:i * 32 + 32]
        df = pd.DataFrame(box)
        state = df[13].value_counts().idxmax()
        cv2.rectangle(originalIMG, (i*32, 55), (i*32+32, 80), (0, 255, 0), 1)
        if state == 0:
            line[i] = 1
    for i in range(1, 4):
        box = img[20:50, i * 32:i * 32 + 32]
        df = pd.DataFrame(box)
        state = df[13].value_counts().idxmax()
        frontLine.append(state)
        cv2.rectangle(originalIMG, (i*32, 20), (i*32+32, 50), (0, 255, 0), 1)
    print(frontLine)
    if 0 in frontLine:
        line[5] = 1
    return line, img, originalIMG


img = cv2.imread('img.png',cv2.IMREAD_GRAYSCALE)
last = time.time()
line, img,originalIMG = processImage(img)
print(line,time.time()-last)
cv2.imshow('originalIMG',img)
cv2.imshow('image',originalIMG)
cv2.waitKey(0)
cv2.destroyAllWindows()