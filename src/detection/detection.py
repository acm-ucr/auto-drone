import cv2
import numpy as np
import time
from paho.mqtt import client as mqtt_client

# This script is the publisher for mqtt

stream_url = "http://10.42.0.107:7123/stream.mjpg"
# cap = cv2.VideoCapture(stream_url)
cap = cv2.VideoCapture(0)

# Cascade data for traffic cones
cone_data = cv2.CascadeClassifier('/home/justin-im/Projects/auto-drone/training/classifier/cascade1.xml')

# Client and broker set up
broker = 'broker.emqx.io'
port = 1883
topic = "Drone Commands"
client_id = f'python-mqtt-{"jiggles"}'

# Array of messages?
msg_array = np.array(["Move Forward", "Move Left", "Move Right", "Move Back", "Move Up", "Move Down"])

def connect_mqtt():
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


def run():
    client = connect_mqtt()
    client.loop_start()

    while(1):
        # Array of CV2 Rectangles dimensions
        max_list = np.empty((10,4))
        
        # Captures the frame and stores found object rectangles in found
        ret, frame = cap.read()
        cv2.imshow("capture", frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found = cone_data.detectMultiScale(gray_frame, minSize = (24, 24), scaleFactor=1.1, minNeighbors=8)
        amount_found = len(found)

        for (x, y, w, h) in found:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        print(f"Amount Found: {amount_found}")

        # Sort by size, take the largest rectangle
        sorted_rects = sorted(found, key=lambda r: r[2] * r[3], reverse=True)
        msg = msg_array[0]
        if (len(sorted_rects) > 0):
            cv2.rectangle(frame, (sorted_rects[0][0], sorted_rects[0][1]), (sorted_rects[0][0] + sorted_rects[0][2], sorted_rects[0][1] + sorted_rects[0][3]), (37, 0, 66), 2)

            # Calculate center coordinates of largest rectangle
            center = (sorted_rects[0][0] + int(sorted_rects[0][2]/2), sorted_rects[0][1] + int(sorted_rects[0][3]/2))
            cv2.circle(frame, center, radius = 2, color=(0, 0, 255), thickness=2)

            if (center[0] > 320):
                # Move Right
                msg = msg_array[2]
            else:
                msg = msg_array[1]



        print(f"Direction Message: {msg}")

        publish(client, msg)

        cv2.imshow("capture", frame)

    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release
    cv2.destroyAllWindows
    client.loop_stop()

if __name__ == '__main__':
    run()