import socket
import _pickle as pickle
import cv2
import numpy as np
import pandas as pd


def startServer():
    HOST = '192.168.43.106'
    PORT = 5000
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')

    try:
        conn.bind((HOST, PORT))
    except socket.error:
        print('Bind failed')
        return False

    conn.listen(5)
    print('Socket awaiting handshake')
    (conn, addr) = conn.accept()
    print('Connected')
    return conn

def processImage(originalIMG):
    _, img = cv2.threshold(originalIMG[30:110, 0:160], 80, 255, cv2.THRESH_BINARY)
    #img = cv2.adaptiveThreshold(originalIMG[30:110, 0:160], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    #_, img = cv2.threshold(originalIMG, 155, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # cv2.imwrite('shadow.png',img)
    # cv2.imwrite('orgi.png',originalIMG)
    line = [0, 0, 0, 0, 0, 0]
    frontLine = []
    originalIMG = originalIMG[30:110, 0:160]
    for i in range(0, 5):
        box = img[55:80, i * 32:i * 32 + 32]
        df = pd.DataFrame(box)
        state = df[13].value_counts().idxmax()
        cv2.rectangle(img, (i*32, 55), (i*32+32, 80), (0, 255, 0), 1)
        if state == 0:
            line[i] = 1
    for l in range(1, 4):
        box = img[20:50, l * 32:l * 32 + 32]
        df = pd.DataFrame(box)
        state = df[13].value_counts().idxmax()
        cv2.rectangle(img, (l * 32, 20), (l * 32 + 32, 50), (0, 255, 0), 1)
        frontLine.append(state)
    if 0 in frontLine:
        line[5] = 1
    return line, img,originalIMG

conn = startServer()
while 1:
    try:
        data = conn.recv(1000000)
        originalImage = np.array(pickle.loads(data))
        lineState, processedIMG,originalImage = processImage(originalImage)
        cv2.imshow('image', originalImage)
        cv2.imshow('Processed Image', processedIMG)
        print(lineState)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        print('error', e)
