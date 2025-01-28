import cv2
import numpy as np
import time
import threading
from queue import Queue
from paho.mqtt import client as mqtt_client

# Array of messages?
msg_array = np.array([0b000, 0b001, 0b010, 0b011, 0b100, 0b101])
frame_queue = Queue(maxsize=30)
result_queue = Queue()
time.sleep(20)
stream_url = "http://10.42.0.107:7123/stream.mjpg"
cap = cv2.VideoCapture(stream_url)

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
    global cone_data

    client = connect_mqtt()
    client.loop_start

    # Cascade data for traffic cones
    cone_data = cv2.CascadeClassifier('/home/justin-im/Projects/auto-drone/training/classifier/cascade1.xml')

def frameCapture():
    counter = 0
    while(1):
        ret, frame = cap.read()
        if not ret:
            print("Frame grab error")

        cv2.imshow("capture", frame)

        # Saves 1 frame out of 10 frames into the queue for analysis
        if counter%10 == 0:
            frame_queue.put(frame)
        else:
            print("Full frame queue, dropping frame")
        counter+=1
        
    
        
def frameAnalysis():
    while(1):
        if not frame_queue.empty():
            frame = frame_queue.get()
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            found = cone_data.detectMultiScale(gray_frame, minSize = (24, 24), scaleFactor=1.1, minNeighbors=3)
            for (x,y,w,h) in found:
                cv2.rectangle(frame, (x, y), (x+2, y+h), (255, 0, 0), 2)
            result_queue.put(found)
        else:
            time.sleep(0.01)

def sendData():
    while(1):
        if not result_queue.empty():
            box = result_queue.get()
            amount_found = len(box)
            if amount_found > 0:
                sorted_rects = sorted(box, key=lambda r: r[2]*r[3], reverse = True)
                center = (sorted_rects[0][0] + int(sorted_rects[0][2]/2, sorted_rects[0][1] + int(sorted_rects[0][3]/2)))

                if center[0] > 320:
                    msg = 1
                    publish(client, msg)
                else:
                    msg = 2
                    publish(client, msg)
                    
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release
    cv2.destroyAllWindows
    client.loop_stop()

if __name__ == '__main__':
    init_thread = threading.Thread(target = init)
    time.sleep(2)
    frameCapture_thread = threading.Thread(target = frameCapture)
    time.sleep(2)
    frameAnalysis_thread = threading.Thread(target = frameAnalysis)
    time.sleep(2)
    sendData_thread = threading.Thread(target = sendData)
    time.sleep(2)

    init_thread.start()
    frameCapture_thread.start()
    frameAnalysis_thread.start()
    sendData_thread.start()

    init_thread.join()
    frameCapture_thread.join()
    frameAnalysis_thread.join()
    sendData_thread.join()

    print("Threads Completed")
    