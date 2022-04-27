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
trackbar_blur = "Blur:"
tmpLineDegrees = []
trackbar_seperation = "Degree seperation:"

def within(val, list_arg, seperation):
	for x in list_arg:
		if val > x-seperation/10 and val < x+seperation/10:
			return True

def probable_division(degree_list):
	# This is a very dirty way to do this, but hopefully I'll be forgiven.
	# How this is supposed to work is that it will bruteforce guess to the closest matching
	# dial indicator face since all dial indicators have a minimum of 10 scale divisions.
	x = len(degree_list) # How many lines where found on the dial face?
	if x <= 0:
		return
	current_guess = 0
	last_value = 180
	loop = True
	while loop:
		#print("x: {}".format(x))
		current_guess += 10
		if 360/current_guess > 360/x:
			last_value = current_guess
		elif 360/current_guess <= 360/x:
			print("Probable solution: {}".format(str(current_guess)))
			loop = False

def testing_fft(degree_list):
	if degree_list == None:
		return
	elif len(degree_list) < 2:
		return
	elif type(degree_list) == type(int()):
		return
	else:
		degree_list.sort()
		diff_list = []
		i = 0
		#for i in degree_list:
		#	print("Testing")
		for i in range(len(degree_list)):
			if i == 0:
				diff_list.append(degree_list[i]-degree_list[len(degree_list)-1]+360) # First item in the list we can't compare against previous
				# item since that would cause a out of bounds read, so just read the last item in the list and calculate the difference.
			elif i < len(degree_list):
				diff_list.append(degree_list[i]-degree_list[i-1])
		for i in diff_list:
			print("%.2f"%i)

def update(val):
	global src
	threshold = cv.getTrackbarPos(trackbar_threshold, window_name)
	minLineLenght = cv.getTrackbarPos(trackbar_minLineLenght, window_name)
	maxLineGap = cv.getTrackbarPos(trackbar_maxLineGap, window_name)
	circle1_value = cv.getTrackbarPos(trackbar_circle1, window_name)
	circle2_value = cv.getTrackbarPos(trackbar_circle2, window_name)
	blur_value = cv.getTrackbarPos(trackbar_blur, window_name)
	seperation_value = cv.getTrackbarPos(trackbar_seperation, window_name)
	if seperation_value < 1 or seperation_value > 40:
		seperation_value = 0
	tmp = src
	if blur_value > 0 and blur_value <= 20:
		tmp = cv.blur(src, (blur_value, blur_value))
	dst = cv.Canny(tmp, 50, 200, None, 3)
	cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
	lines = cv.HoughLinesP(dst, 1, np.pi/180, threshold, None, minLineLenght, maxLineGap)
	if circle1_value > 0:
		cv.circle(cdst, (1320, 1312), circle1_value, (255,255,255), 10)
	if circle2_value > 0:
		cv.circle(cdst, (1320, 1312), circle2_value, (255,0,255), 10)
	if lines is not None:
		tmpLineDegrees.clear()
		plottedLines = []
		for i in range(0, len(lines)):
			l = lines[i][0]
			r1 = math.hypot(l[0]-1320, l[1]-1312)
			r2 = math.hypot(l[2]-1320, l[3]-1312)
			if r1 < circle1_value and r1 > circle2_value or r2 > circle2_value and r2 < circle1_value:
				if seperation_value != 0:
					degrees = math.degrees(math.atan2(l[0]-1320, l[1]-1312))
					if len(plottedLines) == 0:
						cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv.LINE_AA)
						plottedLines.append(degrees)
					else:
						if not within(degrees, plottedLines, seperation_value):
							cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv.LINE_AA)
							plottedLines.append(degrees)
							tmpLineDegrees.append(degrees)
						#for line in plottedLines:
						#	if degrees >= line-seperation_value/10 and degrees <= line-seperation_value/10:
						#		continue
						#	else:
						#		cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv.LINE_AA)
						#		plottedLines.append(degrees)
				#cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,255,0), 3, cv.LINE_AA)
				#tmpLineDegrees.append(math.degrees(math.atan2(l[0]-1320, l[1]-1312)))
		probable_division(plottedLines)
		testing_fft(plottedLines)
	cdstCopy = helper.scale(cdst, 25)
	cv.imshow(window_name, cdstCopy)

#if os.path.exists("degreelogging.txt"):
#	os.remove("degreelogging.txt")
cv.namedWindow(window_name)
cv.createTrackbar(trackbar_threshold, window_name, 100, 100, update)
cv.createTrackbar(trackbar_minLineLenght, window_name, 20, 400, update)
cv.createTrackbar(trackbar_maxLineGap, window_name, 15, 50, update)
cv.createTrackbar(trackbar_circle1, window_name, 1200, 1500, update)
cv.createTrackbar(trackbar_circle2, window_name, 980, 1300, update)
cv.createTrackbar(trackbar_blur, window_name, 3, 20, update)
cv.createTrackbar(trackbar_seperation, window_name, 20, 40, update)
cv.waitKey()
#with open("degreelogging.txt", "w") as f:
#	tmpLineDegrees.sort()
#	for degree in tmpLineDegrees:
#		f.write(str(round(degree, 2))+"\n")