from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import numpy as np
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 16
rawCapture = PiRGBArray(camera, size=(640,480))

# allow the camera to warmup
time.sleep(0.1)

flatArea = 1000
font = cv2.FONT_HERSHEY_SIMPLEX

# fourcc = cv2.VideoWriter_fourcc(*"XVID")
# out = cv2.VideoWriter('trial.avi', fourcc, camera.framerate, (640, 480))

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
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    Z = image.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters (K) and apply kmeans segmentation
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    ret, label, center = cv2.kmeans(Z,K,None,criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((image.shape))

    cv2.imshow("Frame",res2)
    # time.sleep(0.5)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)
    if key == ord("q"):
        break
