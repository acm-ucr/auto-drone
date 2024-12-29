import cv2
import numpy as np
import paho.mqtt.client as mqtt

stream_url = "http://192.168.1.219:7123/stream.mjpg"
# cap = cv2.VideoCapture(stream_url)
cap = cv2.VideoCapture(0)

# Cascade data for traffic cones
stop_data = cv2.CascadeClassifier('training\classifier\cascade.xml')

# Client and broker set up
# client = mqtt.Client("my_client")

# Topic Set Up
topic = "Drone Commands"

# Array of messages?
msg_array = np.array(["Move Forward", "Move Left", "Move Right", "Move Back", "Move Up", "Move Down"])

while(1):
    rect_list = []
    for i in range(10):
        ret, frame = cap.read()
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found = stop_data.detectMultiScale(gray_frame, minSize = (24, 24))
        amount_found = len(found)
        
        # Finds the rectangle with the largest area and appends it to our list. 
        if amount_found > 0:
            max = found[0]
            if amount_found > 1:
                for j in found:
                    if found[j].area() > max.area():
                        max = found[j]
            rect_list.append(max)
        
        # Calculate Average X, Y
        if len(rect_list) == 10:
            avgx = 0
            avgy = 0
            avgh = 0
            avgw = 0
            for j in rect_list:
                avgx += j.x
                avgy += j.y
                avgh += j.height
                avgw += j.width
            avgx = avgx/10
            avgy = avgy/10
            avgh = avgh/10
            avgw = avgw/10
            
            # Display most recent frame with average x, y, height, and width
            cv2.rectangle(frame, (avgx, avgy), (avgx+avgw, avgy+avgh), (255, 0, 0), 2)
            cv2.imshow("tracking", frame)
            
            # Find center of the object
            centerX = avgx + (avgh/2)
            centerY = avgy + (avgw/2)
            
            # Based on center coordinates, switch statement to make a decision
            
            
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release
cv2.destroyAllWindows


    # # Array of Rectanges
    # rect_array = np.array(10)
    # # Generate a coordinate of a cone over 10 frames. 
    # for i in range(10): 
    #     ret, frame = cap.read()

    #     # This should be done after a frame assembled after unpacking from the socket.    
    #     gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    #     found = stop_data.detectMultiScale(gray_frame, minSize = (24, 24))
    #     amount_found = len(found)
    #     if (amount_found != 0) :
    #         # Drone.stop
    #         rect_array = np.array()
    #         for (x, y, w, h) in found:
    #             # Find the largest rectangle, maybe using lidar?
    #             # Store the closest rectangle into rect_array
                
    #             cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #             # Move drone until the object is no longer tracked
    #             # Choose direction based on x, y coordinates relative to 640 x 480 frame
        
    #     # Else, then move drone forward?