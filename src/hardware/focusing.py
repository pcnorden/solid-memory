import cv2 as cv
import numpy as np

# Source of most of this computational code:
# https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/

def variance_of_laplace(src: cv.Mat):
	"""Computes the Laplacian of the image and then returns the focus
	measure, which is simply the variance of Laplacian"""
	cv.Laplacian(src, cv.CV_64F).var()

# Shamelessly taken from https://github.com/opencv/opencv/blob/17234f82d025e3bbfbf611089637e5aa2038e7b8/samples/python/video_v4l2.py#L25
# since I really don't understand what is going on here
def decode_fourcc(v):
	v = int(v)
	return "".join([chr((v >> 8*i)&0xFF) for i in range(4)])

def change_focus(focus: int, capture=None):
	#print(focus*5)
	capture.set(cv.CAP_PROP_FOCUS, focus*5)

def main():
	font = cv.FONT_HERSHEY_SIMPLEX
	color = (0,255,0)

	cap = cv.VideoCapture(2)
	cap.set(cv.CAP_PROP_AUTOFOCUS, 0)

	cv.namedWindow("Video")

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
	print("Done")

if __name__ == "__main__":
	main()