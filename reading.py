import cv2 as cv
import helper
import numpy as np
import math

src = cv.imread("dial_face.jpg")
dst = cv.Canny(src, 50, 200, None, 3)
cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
window_name = "HoughLinesP debugger"
trackbar_threshold = "HoughLinesP threshold:"
trackbar_minLineLenght = "HoughLinesP minLineLenght:"
trackbar_maxLineGap = "HoughLinesP maxLineGap:"
trackbar_circle1 = "Bigger circle:"
trackbar_circle2 = "Smaller circle:"

def update(val):
	global src
	threshold = cv.getTrackbarPos(trackbar_threshold, window_name)
	minLineLenght = cv.getTrackbarPos(trackbar_minLineLenght, window_name)
	maxLineGap = cv.getTrackbarPos(trackbar_maxLineGap, window_name)
	circle1_value = cv.getTrackbarPos(trackbar_circle1, window_name)
	circle2_value = cv.getTrackbarPos(trackbar_circle2, window_name)
	dst = cv.Canny(src, 50, 200, None, 3)
	cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
	lines = cv.HoughLinesP(dst, 1, np.pi/180, threshold, None, minLineLenght, maxLineGap)
	if circle1_value > 0:
		cv.circle(cdst, (1320, 1312), circle1_value, (255,255,255), 10)
	if circle2_value > 0:
		cv.circle(cdst, (1320, 1312), circle2_value, (255,0,255), 10)
	if lines is not None:
		for i in range(0, len(lines)):
			l = lines[i][0]
			r1 = math.hypot(l[0]-1320, l[1]-1312)
			r2 = math.hypot(l[2]-1320, l[3]-1312)
			#print(r1)
			if r1 < circle1_value and r1 > circle2_value or r2 > circle2_value and r2 < circle1_value:
				cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv.LINE_AA)
			#else:
				#cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)
	cdstCopy = helper.scale(cdst, 25)
	cv.imshow(window_name, cdstCopy)

cv.namedWindow(window_name)
cv.createTrackbar(trackbar_threshold, window_name, 100, 100, update)
cv.createTrackbar(trackbar_minLineLenght, window_name, 20, 400, update)
cv.createTrackbar(trackbar_maxLineGap, window_name, 15, 50, update)
cv.createTrackbar(trackbar_circle1, window_name, 1200, 1500, update)
cv.createTrackbar(trackbar_circle2, window_name, 980, 1300, update)
cv.waitKey()