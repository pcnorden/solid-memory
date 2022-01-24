import cv2 as cv

def scale(src, size_percentage: int):
	dsize = (int(src.shape[1]*size_percentage/100), int(src.shape[0]*size_percentage/100))
	return cv.resize(src, dsize)