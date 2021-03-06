#import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
#import
import cv2
import argparse

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help = "path to the (optional) video file")
ap.add_argument("-b", "--buffer",
    type=int, default=64, help="max buffer size")
ap.add_argument("-o", "--outfile",
	type=str, default='trial.avi', help="video file for output")
args = vars(ap.parse_args())

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# allow the camera to warmup
time.sleep(0.1)

outfile = args['outfile']
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter(outfile, fourcc, camera.framerate, (640, 480))

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, the initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	lab = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
	l,a,b = cv2.split(lab)

	# segment stable regions in the a-channel
	# which corresponds to red-green variations within the image
	mser = cv2.MSER_create()
	regions = mser.detectRegions(a, None)
	hulls = [cv2.convexHull(p.reshape(-1,1,2)) for p in regions]
	cv2.polylines(image, hulls, 1, (0, 255, 0))


	# image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# ret, image = cv2.threshold(image, 20, 80,cv2.THRESH_BINARY)

	cv2.imshow("Frame",image)
	data = np.array([time.now(), ])
	# time.sleep(0.5)
	key = cv2.waitKey(1) & 0xFF
	rawCapture.truncate(0)
	if key == ord("q"):
		break
	time.sleep(5)
