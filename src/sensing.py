from ctypes import resize
import sys
import math
import cv2 as cv
import numpy as np
#import reading as fuck
import helper

def detect_outer_ring(src_img):
	"""
	Detects the dial indicator outer ring, be aware though that since it's caluclated using grayscale
	the background needs to be white if the dial is black.
	
	If dial case is white, black background is needed.

	Warning: this function isn't fast nor well-tuned! Absolutely do not call this in a UI thread!
	
	Arguments:
	* `src_img`: The original image that was loaded from either harddrive or a camera stream.

	Returns:
	* `None` incase there was no circle found (or too many of them).
	* `Array` array containing Y, X and radius of the circle found in the image.
	"""
	src = src_img # Make a copy of the input file so we can modify it incase we need to debug parameters
	gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY) # Convert to grayscale so we can mangle the HoughCircles input better
	gray = cv.medianBlur(gray, 5) # Incase there are any small imperfections, blur the image a bit.
	rows = gray.shape[0] # Get the height of the image
	circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows/2, param1=300, param2=70, minRadius=800, maxRadius=2000) 
	if circles is not None: # Did we get good results?
		circles = np.uint16(np.around(circles)) # Round the values to whole numbers and store it in a uin16 array
		if len(circles) > 1: # Debugging logic incase we need to tune the parameters incase we detect several circles in the same image.
			print("Found more than 1 circle! showing image for tweaking of parameters!")
			for i in circles[0, :]:
				# Circle center
				cv.circle(src, (i[0], i[1]), 1, (255, 0, 255), 10)
				# Circle outline
				cv.circle(src, (i[0], i[1]), i[2], (255, 0, 255), 10)
			resized = helper.scale(src, 20) # Scale the image down so we don't show a huge image on a small laptop screen.
			cv.imshow("Debugging outer ring params", resized) # Show the image with the drawn circles on it.
			cv.waitKey()
			return None # Tell the program we failed to identify a single circle.
		#print("Found {} circles!".format(len(circles)))
		for i in circles[0, :]:
			# Return the first circle since we have already checked how many circles we've detected before this code.
			# Return Y, X and radius of the circle.
			return [i[0], i[1], i[2]]
	else:
		return None

def crop_to_dial_face(src, y, x, r):
	rowsMin = x-r
	rowsMax = x+r
	columnsMin = y-r
	columnsMax = y+r
	# Just checking that all the data is valid and not a point outside the image.
	if rowsMin < 0:
		rowsMin = 0
	if rowsMax > src.shape[0]:
		rowsMax = src.shape[0] # Set as image height
	if columnsMin < 0:
		columnsMin = 0
	if columnsMax > src.shape[1]:
		columnsMax = src.shape[1]
	
	# Finally crop the image, though note that it's [rows, columns] in opencv
	return src[rowsMin:rowsMax, columnsMin:columnsMax]
	

def detect_dial_mounting(src_img):
	src = src_img
	gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
	gray = cv.medianBlur(gray, 5)
	rows = gray.shape[0]
	circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows/3, param1=150, param2=70, minRadius=40, maxRadius=200)
	if circles is not None:
		circles = np.uint16(np.around(circles))
		if len(circles) > 1:
			print("Too many circles in trying to identify dial indicator center! Showing debug image")
			for i in circles[0, :]:
				cv.circle(src, (i[0], i[1]), 1, (255, 0, 255), 10) # Center point
				cv.circle(src, (i[0], i[1]), i[2], (255, 0, 255), 10) # Outline
			cv.imshow("Detect_dial_mounting debug", src)
			cv.waitKey()
			return None
		for i in circles[0, :]:
			return [i[0], i[1], i[2]]
	else:
		return None

def showQuick(img, title="Testing"):
	testing = helper.scale(img, 30)
	cv.imshow(title, testing)
	cv.waitKey()

def process_face_lines(src_img):
	src = src_img
	#showQuick(src, "Source image copy")
	dst = cv.Canny(src, 50, 200, None, 3)
	#showQuick(dst, "DST Testing")
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

def circle_processing(argv):
	default_file = "dial_2.jpg"
	src = cv.imread(default_file, cv.IMREAD_COLOR)
	# Check if image loaded OK
	if src is None:
		print("Image failed to load")
		return -1
	"""
	Detect the outer dial face first, because we will use that as a reference
	to try to find the place where the indicator center is located by cropping the image
	a lot to around the center area so we won't have as many false positives.
	"""
	outer_dial_center = detect_outer_ring(src)
	if outer_dial_center is None:
		print("Failed to find any circles, aborting!")
		return -1
	# Retrieve X, Y and radius of the outer casing that was found (hopefully)
	y, x, r = outer_dial_center[0], outer_dial_center[1], outer_dial_center[2]
	print("Y: {}, X: {}, R: {}".format(x, y, r))
	crop_img = crop_to_dial_face(src, y, x, r)
	
	# Do the same as above, except this time make it snappy and on the cropped dial face.
	y, x, r = detect_dial_mounting(crop_img)
	print("X: {}, Y: {}, R: {}".format(y, x, r))
	plotted_lines_img = helper.scale(process_face_lines(crop_img), 30)
	cv.imshow("Plotted face lines", plotted_lines_img)
	cv.waitKey()
	#fuck.show(crop_img)
	return 0

def main(argv):
	# https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html
	scale_percentage = 25
	default_file = "dial.jpg"
	filename = argv[0] if len(argv) > 0 else default_file

	#Load the image
	src = cv.imread(filename, cv.IMREAD_GRAYSCALE)

	# Check if image loaded successfully
	if src is None:
		print("Error opening image!")
		return -1

	dst = cv.Canny(src, 50, 200, None, 3)

	# Copy edges to the images that will display the results in BGR
	cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)

	linesP = cv.HoughLinesP(dst, 1, np.pi/180, 50, None, 40, 15)
	if linesP is not None:
		numb = len(linesP)
		print("Found {} lines".format(numb))
		for i in range(0, len(linesP)):
			l = linesP[i][0]
			cv.line(cdst, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv.LINE_AA)

	cdst = helper.scale(cdst, scale_percentage)
	cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdst)
	cv.waitKey()
	return 0

if __name__ == "__main__":
	if len(sys.argv) > 1:
		if sys.argv[1] == "reading":
			import reading
		else:
			circle_processing(sys.argv[1:])
	else:
		#main(sys.argv[1:])
		circle_processing(sys.argv[1:])

# https://docs.opencv.org/4.x/d4/d70/tutorial_hough_circle.html
# https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html