# python flat tracking
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# declare global variables
minTraySize = 5000

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help = "path to the (optional) video file")
ap.add_argument("-b", "--buffer",
    type=int, defaul=64, help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# trays in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the camera
if not args.get("video", False):
    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640,480))
else:
    camera = cv2.VideoCapture(args["video"])

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    blurred = cv2.GaussianBlur(frame, (11,11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        box = cv2.boxPoints(c)
        box = np.int0(box)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        if cv2.contourArea([box]) >= minTraySize:
