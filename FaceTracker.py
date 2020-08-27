#!/usr/bin/python3

import cv2
import urllib.request
import numpy as np
import websocket
import math
import time

host = 'localhost'

stream = urllib.request.urlopen('http://' + host + ':81?action=stream')
command_socket = websocket.create_connection('ws://' + host + ':82')
data = bytes()

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

current_command = ''

next_action_time = 0

while True:
    data += stream.read(1024)
    a = data.find(b'\xff\xd8')
    b = data.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = data[a:b + 2]
        data = data[b + 2:]
        frame = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

        faces = face_cascade.detectMultiScale(
            frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
        )

        centerX = 320
        centerY = 240

        deadzone = 60

        def send_command(command):
            global current_command
            if command == current_command:
                return
            current_command = command
            print("sending command: " + command)
            command_socket.send(command)


        if faces.__len__() == 0:
            send_command('stop')
        else:
            (x, y, w, h) = faces[0]
            faceX = int(x + w / 2)
            faceY = int(y + h / 2)

            difX = faceX - centerX
            difY = faceY - centerY

            distance = math.sqrt(
                difX * difX
                + difY * difY
            )

            now = time.time()
            if now > next_action_time:
                if distance < 40:
                    send_command("fire")
                    next_action_time = now + 4.2
                elif abs(difX) > deadzone:
                    send_command("right" if difX > 0 else "left")
                elif abs(difY) > deadzone:
                    send_command("down" if difY > 0 else "up")
                else:
                    send_command("stop")

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.line(frame, (centerX, centerY), (faceX, faceY), (0, 255, 0), 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) == 27:
            exit(0)
