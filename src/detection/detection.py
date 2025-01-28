import cv2
import numpy as np
import time
import threading
from queue import Queue
from paho.mqtt import client as mqtt_client

# Array of messages?
msg_array = np.array([000, 001, 010, 011, 100, 101])
frame_queue = Queue(maxsize=30)
result_queue = Queue()

def connect_mqtt():
    global topic

    broker = 'broker.emqx.io'
    port = 1883
    topic = "Drone Commands"
    client_id = f'python-mqtt-{"jiggles"}'
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, msg):
    time.sleep(1)
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

def init():
    # Client and broker set up

    global client
    global cap
    global cone_data

    client = connect_mqtt()
    client.loop_start
    # Delay so that local host can set up
    time.sleep(20)
    stream_url = "http://10.42.0.107:7123/stream.mjpg"
    cap = cv2.VideoCapture(stream_url)
    # Cascade data for traffic cones
    cone_data = cv2.CascadeClassifier('/home/justin-im/Projects/auto-drone/training/classifier/cascade1.xml')

def frameCapture():
    counter = 0
    while(1):
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        if not ret:
            print("Frame grab error")

        # Saves 1 frame out of 10 frames into the queue for analysis
        if counter%10 == 0:
            frame_queue.put(frame)
        else:
            print("Full frame queue, dropping frame")
        
def frameAnalysis():
    while(1):
        if not frame_queue.empty():
            frame = frame_queue.get()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found = cone_data.detectMultiScale(gray_frame, minSize = (24, 24), minNeighbors=3)
            result_queue.put(found)
        else:
            time.sleep(0.01)

def sendData():
    while(1):
        if not result_queue.empty():
            box = result_queue.get()
            amount_found = len(box)
            if amount_found > 0:



def run():
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
                object_center_x = avgx + int(avgw/2)
                object_center_y = avgy + int(avgh/2)
                
                
                # Ignore instances where the average area is less than a something, arbitrarily chose 50 x 50
                msg = msg_array[0]
                if (avgx > 100 and avgy > 100):
                    # Based on center coordinates relative to center of 640x480p camera feed, switch statement to make a decision
                    if (avgx > 320):
                        # Move Right
                        msg = msg_array[2]
                    else:
                        # Move Left (also by default)
                        msg = msg_array[1]

                print(f"Direction Message: {msg}")
                
                # Broadcast message
                publish(client, msg)
    
                # Reset counter
                counter = 0
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release
    cv2.destroyAllWindows
    client.loop_stop()

if __name__ == '__main__':
    run()