# Author: Erik Priest (eriktpriest@gmail.com |  Github: Erik Priest)
#
# Purpose: This file is intended to be the main communication point between
#       the ethernet camera the website to display tracking data. This file
#       will steam in the camera data from ethernet, process and track targets
#       then will report it to the MQTT services
#
# Args: [optional]
#       -v [video file path] # reads video file path for model prediction
#       -vr [video file path] # reads video file path for model prediction and repeats messages until q is pressed
#       -i [image file path] # reads image file path for model prediction

__author__ = 'Erik Priest'

import yaml
import json
import sys
import socket
import time
import cv2
import numpy as np
from ultralytics import YOLO
import paho.mqtt.client as paho
from paho import mqtt
import tracking

_my_uuid = ""


## Start: MQTT callbacks ##
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)


def on_disconnect(self, client, userdata, rc):
    if rc != 0:
        print("Disconnected")


def on_publish(client, userdata, mid, properties=None):
    # print("mid:" + str(mid))
    return


def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
## End: MQTT callbacks ##


def publish_data(json_msg):
    ret = client.publish("taugroup/{uuid}".format(uuid=_my_uuid), json_msg, qos=1)
    return ret


def camera_predict(model):
    camera = cv2.VideoCapture(0)

    while (True):
        # Capture frame-by-frame
        ret, frame = camera.read()

        if frame is not None:
            results = tracking.track_frame(model, frame, 0)
            json_data = tracking.write_json(results, 0, frame.shape)
            # Send json_data to MQTT service
            json_msg = json.dumps(json_data)
            publish_data(json_msg)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    camera.release()
    cv2.destroyAllWindows()


def image_predict(model, path):
    try:
        image = cv2.imread(path)
        results = tracking.track_frame(model, image, 0)
        json_data = tracking.write_json(results, 0, image.shape)
        json_msg = json.dumps(json_data)
        publish_data(json_msg)
    except IOError as strerror:
        print("I/O error in image predicition: {0}".format(strerror))
        exit()


def video_predict(model, path):
    json_data = []
    vid_capture = cv2.VideoCapture(path)

    prev_time = 0
    counter = 0
    while (vid_capture.grab()):
        client.loop()
        ret, frame = vid_capture.read()
        time_elapsed = time.time() - prev_time

        if time_elapsed > (1.0 / frame_rate) and ret is True:
            prev_time = time.time()
            results = tracking.track_frame(model, frame, counter)
            json_raw = tracking.write_json(results, counter, frame.shape)
            json_msg = json.dumps(json_raw)
            json_data.append(json_msg)
            client.publish("taugroup/{uuid}".format(uuid=_my_uuid), json_msg, qos=1)
            counter += 1

    try:
        with open('output.json', 'w') as f:
            json.dump(json_data, f, indent=4)
    except IOError as strerror:
        print("I/O error: {0}".format(strerror))


def video_predict_repeat(model, path):
    json_data = []
    vid_capture = cv2.VideoCapture(path)
    prev_time = 0
    counter = 0

    while (vid_capture.grab()):
        client.loop()
        ret, frame = vid_capture.read()
        time_elapsed = time.time() - prev_time

        if time_elapsed > (1.0 / frame_rate) and ret is True:
            prev_time = time.time()
            results = tracking.track_frame(model, frame, counter)
            json_raw = tracking.write_json(results, counter, frame.shape)
            json_msg = json.dumps(json_raw)
            json_data.append(json_msg)
            publish_data(json_msg)
            counter += 1

    while (True):
        rc = client.loop()
        if rc != paho.MQTT_ERR_SUCCESS:
            try:
                time.sleep(1.0)
                client.reconnect()
            except (socket.error, paho.WebsocketConnectionError):
                continue

        for json_msg in json_data:
            time.sleep(1.0 / frame_rate)
            publish_data(json_msg)
            client.loop()


def load_config():
    # Dictionary for config file
    _config = {}

    # Try to read data from the config file
    try:
        with open("backend/settings.yaml", "r") as f:
            _config = yaml.safe_load(f)
    except IOError as strerror:
        print("I/O error: {0}".format(strerror))
        exit()

    return _config


if __name__ == '__main__':

    _config = load_config()

    yolo_model = YOLO(_config["YOLO_MODEL"])  # load official detection model
    frame_rate = float(_config["FRAME_RATE"])

    # Connect to MQTT services
    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect  # Add callback

    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("nistai3", "nistpscrai3")
    client.connect("030a29b11d714f4dae6fb60c9ab4a2c5.s1.eu.hivemq.cloud", 8883)

    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    ##

    json_msg = []
    _my_uuid = 'smart_farm'

    # sys args
    if len(sys.argv) > 1:
        command = sys.argv[1]  # extract command
        file_path = sys.argv[2]
        _my_uuid = sys.argv[4]

        if command == "-v":
            # run video prediction
            video_predict(yolo_model, file_path)
        elif command == "-vr":
            # run image prediction
            video_predict_repeat(yolo_model, file_path)
        elif command == "-i":
            # run image prediction
            image_predict(yolo_model, file_path)
        else:
            # Exit if not of valid command type
            print("Invalid argument")
            print("Valid arguments are:")
            print("python3 main.py          # use default camera device")
            print("python3 main.py -v [video file path]")
            print("python3 main.py -i [image file path]")
            exit()
    else:
        # Run default setup which is camera 0
        json_msg = camera_predict(yolo_model)
