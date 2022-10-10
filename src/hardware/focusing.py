import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time

def getColorChannels(src: cv.Mat) -> int:
	"""Returns how many color channels a provided image has."""
	if len(src.shape) == 2:
		return 1
	elif len(src.shape) == 3:
		return src.shape[2]
	else:
		raise ValueError("Image shape has unknown shape data in it!")

# Source of most of this computational code:
# https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/

def variance_of_laplace(src: cv.Mat):
	"""Computes the Laplacian of the image and then returns the focus
	measure, which is simply the variance of Laplacian"""
	if getColorChannels(src) != 1:
		raise ValueError("Got a color image when expecting a grayscale image!")
	return cv.Laplacian(src, cv.CV_64F).var()

# Shamelessly taken from https://github.com/opencv/opencv/blob/17234f82d025e3bbfbf611089637e5aa2038e7b8/samples/python/video_v4l2.py#L25
# since I really don't understand what is going on here
def decode_fourcc(v):
	v = int(v)
	return "".join([chr((v >> 8*i)&0xFF) for i in range(4)])

def change_focus(focus: int, capture_device):
	"""Allows the focus to be changed between 0 and 51. More or less will result in a ValueError"""
	if focus < 0 or focus > 51:
		raise ValueError("Focus is more than 51 or less than 0!")
	capture_device.set(cv.CAP_PROP_FOCUS, focus*5)

def get_blur_at(focusLevel: int, capture_device):
	cap = cv.VideoCapture(2)
	cap.set(cv.CAP_PROP_AUTOFOCUS, 0) # Disable autofocus so we can manually control it
	cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280) # Set the image width
	cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720) # Set the image height
	for i in range(0,10):
		_status, _img = cap.read() # Let the camera stabilize itself by reading 10 frames
	# Grab a single frame of the video, convert to gray-scale and hand it off to Laplacian variance
	_status, img = cap.read()
	fourcc = decode_fourcc(cap.get(cv.CAP_PROP_FOURCC))
	if fourcc == "MJPG":
		img = cv.imdecode(img, cv.IMREAD_GRAYSCALE)
	elif fourcc == "YUYV":
		img = cv.cvtColor(img, cv.COLOR_YUV2GRAY_YUYV)
	else:
		print("Unsupported format")
	fm = variance_of_laplace(img)

def main():
	font = cv.FONT_HERSHEY_SIMPLEX
	color = (0,255,0)

	cap = cv.VideoCapture(2)
	cap.set(cv.CAP_PROP_AUTOFOCUS, 0)
	# Set the video size to capture 1080p images from the 1080p capable camera
	cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
	cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
	# Add a way to get 30 fps video also since opencv limits the camera to 5 FPS right now

	cv.namedWindow("Video", cv.WINDOW_NORMAL) # A way to view 1080p images in a normal window

	convert_rgb = True
	fps = int(cap.get(cv.CAP_PROP_FPS))
	focus = int(min(cap.get(cv.CAP_PROP_FOCUS)*100, 2**31-1))

	cv.createTrackbar("FPS", "Video", fps, 30, lambda v: cap.set(cv.CAP_PROP_FPS, v))
	cv.createTrackbar("Focus", "Video", focus, 51, lambda v: cap.set(cv.CAP_PROP_FOCUS, v*5))
	while True:
		_status, img = cap.read()

		fourcc = decode_fourcc(cap.get(cv.CAP_PROP_FOURCC))
		fps = cap.get(cv.CAP_PROP_FPS)

		if not bool(cap.get(cv.CAP_PROP_CONVERT_RGB)):
			if fourcc == "MJPG":
				img = cv.imdecode(img, cv.IMREAD_GRAYSCALE)
			elif fourcc == "YUYV":
				img = cv.cvtColor(img, cv.COLOR_YUV2GRAY_YUYV)
			else:
				print("Unsupported format")
				break
		cv.putText(img, "Mode: {}".format(fourcc), (15,40), font, 1.0, color)
		cv.putText(img, "FPS: {}".format(fps), (15,80), font, 1.0, color)
		cv.imshow("Video", img)
		k = cv.waitKey(1)
		if k == 27:
			break
		elif k == ord('g'):
			convert_rgb = not convert_rgb
			cap.set(cv.CAP_PROP_CONVERT_RGB, 1 if convert_rgb else 0)
		if cv.getWindowProperty("Video", cv.WND_PROP_VISIBLE) < 1:
			break

if __name__ == "__main__":
	#main()
	cap = cv.VideoCapture(2)
	if cap.isOpened() == False:
		print("No webcam connected, aborting")
		exit(0)
	cap.set(cv.CAP_PROP_AUTOFOCUS, 0) # Disable autofocus so we can manually control it
	cap.set(cv.CAP_PROP_FOCUS, 0) # Set focus to 0 from the start
	cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280) # Set the image width
	cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720) # Set the image height
	cap.set(cv.CAP_PROP_CONVERT_RGB, 0) # Only use gray-scale image
	for i in range(0,10):
		_status, _img = cap.read() # Let the camera stabilize itself by reading 10 frames
	x = []
	y = []
	#cv.namedWindow("Testing")
	# Grab a single frame of the video, convert to gray-scale and hand it off to Laplacian variance
	for i in range(0, 52):
		print("Loop {} out of 51".format(i))
		change_focus(i, cap)
		#time.sleep(0.5)
		# Get around OpenCV's buffering
		for heck in range(0,10):
			cap.read() # Read 9 images just to clear out the buffer and so we get new pictures
		_status, img = cap.read()
		fourcc = decode_fourcc(cap.get(cv.CAP_PROP_FOURCC))
		if not bool(cap.get(cv.CAP_PROP_CONVERT_RGB)):
			if fourcc == "MJPG":
				img = cv.imdecode(img, cv.IMREAD_GRAYSCALE)
			elif fourcc == "YUYV":
				img = cv.cvtColor(img, cv.COLOR_YUV2GRAY_YUYV)
			else:
				print("Unsupported format")
		#cv.imshow("Testing", img)
		#key = cv.waitKey(5000)
		#if key == 27: # Esc
		#	exit(0)
		#if cv.getWindowProperty("Testing", cv.WND_PROP_VISIBLE) < 1:
		#	exit(0)
		fm = variance_of_laplace(img)
		if fm == None:
			raise ValueError("Something ain't right with the image given to laplace variance!")
		x.append(i)
		y.append(variance_of_laplace(img))
		#print("{}:{}".format(i, variance_of_laplace(img)))
	plt.style.use('dark_background')
	fig, ax = plt.subplots()
	ax.plot(x, y, linewidth=2.5)
	plt.show()
	cap.set(cv.CAP_PROP_AUTOFOCUS, 1) # Enable autofocus again so focusing won't smash the sensor
	time.sleep(0.5) # Wait a bit before we release the handle
	cap.release()