import socket
import sys
import cv2
import pickle
import numpy as np
import struct

stream_url = "http://192.168.1.219:7123/stream.mjpg"
cap = cv2.VideoCapture(stream_url)

# Cascade data for traffic cones
stop_data = cv2.CascadeClassifier('cascade.xml')

while(1):
    ret, frame = cap.read()

    # This should be done after a frame assembled after unpacking from the socket.    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    found = stop_data.detectMultiScale(gray_frame, minSize = (20, 20))
    amount_found = len(found)
    if (amount_found != 0) :
        for (x, y, w, h) in found:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
    # Move drone until the object is no longer tracked?

    cv2.imshow("tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release
cv2.destroyAllWindows