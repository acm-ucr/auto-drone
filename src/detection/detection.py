import cv2
import numpy as np

stream_url = "http://10.42.0.107:7123/stream.mjpg"
# cap = cv2.VideoCapture(stream_url)
cap = cv2.VideoCapture(stream_url)

# Cascade data for traffic cones
cone_data = cv2.CascadeClassifier('/home/justin-im/Projects/auto-drone/training/classifier/cascade1.xml')

while(1):
    ret, frame = cap.read()

    # This should be done after a frame assembled after unpacking from the socket.    
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    found = cone_data.detectMultiScale(gray_frame, minSize = (24, 24))
    amount_found = len(found)
    if (amount_found != 0) :
        # Drone.stop
        for (x, y, w, h) in found:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # Move drone until the object is no longer tracked
            # Choose direction based on x, y coordinates relative to 640 x 480 frame
    
    # Else, then move drone forward?
            


    cv2.imshow("tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release
cv2.destroyAllWindows