import socket
import cv2
import _pickle as pickle

HOST = '192.168.43.106'
PORT = 5000 
conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((HOST,PORT))

cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)

while True:
    try:
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        data = pickle.dumps(frame)
        conn.send(data)
    except:
        break

cap.release()
conn.close()