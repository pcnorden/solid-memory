import cv2 as cv
import math
import numpy as np

def scale(src, size_percentage: int):
	dsize = (int(src.shape[1]*size_percentage/100), int(src.shape[0]*size_percentage/100))
	return cv.resize(src, dsize)

def extract_bars(src: cv.Mat, outer_radius: int, inner_radius: int, block_size: int, blur_kernel_size: int):
	"""Takes a black-and-white image, runs filtering
	and some correction from the filtering and then detects the
	X-Y position of the graduations on a dial face.
	
	@param src: Black and white image that only contains a single color channel.
	
	@param outer_radius: This is the same `outer_radius` that `mask_outside()` was called with.
	
	@param inner_radius: This is the same `inner_radius` that `mask_outside()` was called with.

	@param block_size: The block size that shall be used in `adaptiveThreshold()`. Needs to be a number that isn't divisible by 2!

	@param blur_kernel_size: The kernel size that shall be used when blurring the image before extracting contours. This needs to be a number that isn't divisible by 2!

	@returns Either `None` or a array that looks like this: [(x,y),(x,y)] where each element is a detected point
	"""
	# TODO: Learn more about the parameters and what they do so we don't have to guess values for
	# everything in this script!

	# First, we will check that blur_kernel_size really is not divisible, otherwise throw a exception
	if(blur_kernel_size%2 == 0):
		raise ValueError("blur_kernel_size can't be a even number!")

	# First, we will run some adaptive thresholding on the image to make sure we get a "good"
	# difference between black and white so gray elements won't confuse anything
	img = cv.adaptiveThreshold(src, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, block_size, 5)

	# Next we will remove the 2 circles that the adaptiveThreshold created from the image
	# This is why we need the outer_radius and inner_radius from the call to "mask_outside"
	# Unfortunately for this, we need to again calculate the center point of the image
	hh,ww = src.shape[:2]
	y_center = hh/2
	x_center = ww/2
	# Remove the borders created by adaptiveThreshold finally
	img = cv.circle(img, (x_center, y_center), outer_radius, (255,255,255), 5)
	img = cv.circle(img, (x_center, y_center), inner_radius, (255,255,255), 5)

	# Now we will finally blur the image which will remove a lot of extra contours
	# that would otherwise would show up
	img = cv.GaussianBlur(img, (blur_kernel_size, blur_kernel_size), 0)

	# Now we will run a Otsu threshold operation on the blurred image.
	computed_threshold, image = cv.threshold(img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
	# The above threshold operation would leave the image with a white background
	# and the graduations would be black, but the findContours calls excepts the
	# features we want to detect to be white and the background to be black, so we
	# need to invert the image.
	image = cv.bitwise_not(image)
	# Now it's finally time to extract all the contours in the image. This will be done
	# using OpenCV's 'findCountours()' which is just absolutely amazing in the amount of
	# options I don't understand how to use at all!
	contours, hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
	returnContours = []
	for contour in contours:
		# We shall iterate through the found contours and feed them through a OpenCV
		# function called 'cv.minAreaRect', which finds the smallest possible fitting
		# rect around the contour, then we will take the center points of the rects
		# and return them to the calling function.
		rect = cv.minAreaRect(contour)
		returnContours.append((int(rect[0][0]), int(rect[0][1]))) # Extracts the X and Y positions
	return returnContours # Returns the points to the calling function.

def mask_outside(src: cv.Mat, outer_radius: int, inner_radius: int) -> cv.Mat:
	"""
	Masks away the inner and outer portions of a grayscale image.

	Center position of all is in the image center point, automatically
	calculated.
	"""
	# Calculate where the center point of the provided image is
	hh,ww = src.shape[:2]
	y_center = hh/2
	x_center = ww/2

	# Create a black image that we can start to scribble on of the same size as the input image.
	mask = np.zeros_like(src)
	# Create the biggest circle first that is white and filled
	mask = cv.circle(mask, (x_center, y_center), outer_radius, (255,255,255), cv.FILLED)
	# Create a smaller circle inside the white circle that is black to hide the needle and more.
	mask = cv.circle(mask, (x_center, y_center), inner_radius, (0,0,0), cv.FILLED)
	# Fill the white area drawn above with the image context from @src image
	# and return the result to the calling function
	return cv.bitwise_and(src, mask)

def maxLineLength(line: np.ndarray, maxLineLength: int) -> bool:
	"""
	Takes a line returned from a `cv2.HoughLinesP` and checks if it's
	length is larger than `maxLineLength`.

	Returns `True` incase the line given is less than or equal to `maxLineLength`
	"""
	point1 = (line[0][0], line[0][1])
	point2 = (line[0][2], line[0][3])
	return math.dist([point1, point2]) <= maxLineLength