from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# allow the camera to warmup
time.sleep(0.1)

flatArea = 1000
font = cv2.FONT_HERSHEY_SIMPLEX

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter('trial.avi', fourcc, camera.framerate, (640, 480))

class FlatDetector:
    def __init__(self):
        pass
    def detect(self, c):
        pass

flatFinder = FlatDetector()

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, the initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array
