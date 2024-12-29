import cv2
import numpy as np
import paho.mqtt.client as mqtt

stream_url = "http://192.168.1.219:7123/stream.mjpg"
# cap = cv2.VideoCapture(stream_url)
cap = cv2.VideoCapture(0)

# Cascade data for traffic cones
cone_data = cv2.CascadeClassifier('training\classifier\cascade.xml')

# Client and broker set up
# client = mqtt.Client("my_client")

# Topic Set Up
topic = "Drone Commands"

# Array of messages?
msg_array = np.array(["Move Forward", "Move Left", "Move Right", "Move Back", "Move Up", "Move Down"])

# Array of CV2 Rectangles
rect_list = []
while(1):
    ret, frame = cap.read()
    cv2.imshow("capture", frame)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found = cone_data.detectMultiScale(gray_frame, minSize = (24, 24))
    amount_found = len(found)
    
    # Finds the rectangle with the largest area and appends it to our list. 
    if amount_found > 0:
        print(f"Amount Found: {amount_found}")
        start_point = (found[0][0], found[0][1])
        end_point = (found[0][0] + found[0][2], found[0][1] + found[0][3])
        max = cv2.rectangle(frame, start_point, end_point, (0,0,255), 2)
        
        max_area = found[0][1] * found[0][3]
        for j in found:
            rect_area = (j[2] * j[3])
            
            if rect_area > max_area:
                rect_start_point = (j[0], j[1])
                rect_end_point = (j[0] + j[2], j[1] + j[3])
                rect = cv2.rectangle(frame, rect_start_point, rect_end_point, (0,0,255), 2)
                max = rect
        rect_list.append(max)
        
        # Calculate Average X, Y
        if len(rect_list) == 10:
            avgx = 0
            avgy = 0
            avgh = 0
            avgw = 0
            for j in rect_list:
                avgx = avgx + j[0]
                avgy = avgy + j[1]
                avgw = avgw + j[2]
                avgh = avgh + j[3]   
            avgx = avgx/10
            print(f"avgx: {avgx}")
            avgy = int(avgy/10)
            avgh = int(avgh/10)
            avgw = int(avgw/10)
            
            # Display most recent frame with average x, y, height, and width
            cv2.rectangle(frame, (avgx, avgy), (avgx+avgw, avgy+avgh), (255, 0, 0), 2)
            cv2.imshow("tracking", frame)
            
            # Find center of the object
            centerX = avgx + (avgh/2)
            centerY = avgy + (avgw/2)
            
            # Based on center coordinates, switch statement to make a decision
            
            # Clear list for the next cycle
            rect_list.clear()
        
     
            
            
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