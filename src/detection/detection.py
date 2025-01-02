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

# Counter value
counter = 0

while(1):

    # Array of CV2 Rectangles dimensions
    max_list = np.empty((10,4))
    
    # Captures the frame and stores found object rectangles in found
    ret, frame = cap.read()
    cv2.imshow("capture", frame)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    found = cone_data.detectMultiScale(gray_frame, minSize = (24, 24))
    amount_found = len(found)
    print(f"Amount Found: {amount_found}")
    
    # Finds the rectangle with the largest area and appends it to our list
    if amount_found > 0:
        # Get the first maximum area
        max = np.array([found[0][0], found[0][1], found[0][2], found[0][3]])
        max_area = found[0][2] * found[0][3]
        
        # Checks the rest of the found rectangles for the maximum area
        for i in range(amount_found):
            area = found[i][2] * found[i][3]
            if max_area < area:
                max = np.array([found[i][0], found[i][1], found[i][2], found[i][3]])
                max_area = area
        
        # Populates the correct row of max_list with the values of the maximum rectangle
        for i in range(4):
            max_list[counter][i] = max[i]
            
        counter = counter + 1
        print(f"Counter: {counter}")
        
        # Calculate Average X, Y
        if counter == 10:
            avgx, avgy, avgw, avgh = 0, 0, 0, 0
            for i in range(10):
                avgx += max_list[i][0]
                avgy += max_list[i][1]
                avgw += max_list[i][2]
                avgh += max_list[i][3]
            
            avgx = int(avgx/10)
            print(f"Average x: {avgx}")
            avgy = int(avgy/10)
            print(f"Average y: {avgy}")
            avgw = int(avgw/10)
            print(f"Average w: {avgw}")
            avgh = int(avgh/10)            
            print(f"Average h: {avgh}")
        
            # Display most recent frame with average x, y, height, and width
            cv2.rectangle(frame, (int(avgx), int(avgy)), (int(avgx+avgw), int(avgy+avgh)), (255, 0, 0), 2)
            cv2.imshow("capture", frame)
            
            # Find center of the object
            
            # Based on center coordinates, switch statement to make a decision
            
            # Clear list for the next cycle
            
            # Reset counter
            counter = 0
   
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