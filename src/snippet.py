import cv2 as cv
import helper
import numpy as np

def face_lines(src_img):
	src = src_img
	dst = cv.Canny(src, 50, 200, None, 3)
	cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
	lines = cv.HoughLinesP(dst, 1, np.pi/180, 80, None, 90, 10)
	if lines is not None:
		print("Found {} lines on dial face.".format(len(lines)))
		for i in range(0, len(lines)):
			l = lines[i][0]
			cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0, 0, 255), 3, cv.LINE_AA)
		return cdst
	else:
		return None

max_value = 255
max_type = 4
max_binary_value = 255
trackbar_type = 'Type: \n 0: Binary \n 1: Binary Inverted \n 2: Truncate \n 3: To Zero \n 4: To Zero Inverted'
trackbar_value = 'Value'
window_name = "Threshold Demo"
trackbar_radius = "Diameter"

def Threshold_Demo(val):
	# 0: Binary
	# 1: Binary Inverted
	# 2: Threshold Truncated
	# 3: Threshold to Zero
	# 4: Threshold to Zero Inverted
	threshold_type = cv.getTrackbarPos(trackbar_type, window_name)
	threshold_value = cv.getTrackbarPos(trackbar_value, window_name)
	radius = cv.getTrackbarPos(trackbar_radius, window_name)
	_, dst = cv.threshold(src_gray, threshold_value, max_binary_value, threshold_type)
	cv.circle(dst, (1312,1320), radius, 255, 10)
	dst = helper.scale(dst, 30)
	cv.imshow(window_name, dst)

src = cv.imread("dial_face.jpg")
src_gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
cv.namedWindow(window_name)
cv.createTrackbar(trackbar_type, window_name, 3, max_type, Threshold_Demo)
cv.createTrackbar(trackbar_value, window_name, 0, max_value, Threshold_Demo)
cv.createTrackbar(trackbar_radius, window_name, 1, 1300, Threshold_Demo)
Threshold_Demo(0)
cv.waitKey()
