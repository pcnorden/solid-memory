import cv2 as cv
import numpy as np

algo = "MOG2" # MOG2 or KNN

def background_removal(algo: str):
	if algo == "MOG2":
		backSub = cv.createBackgroundSubtractorMOG2()
	else:
		backSub = cv.createBackgroundSubtractorKNN()
	capture = cv.VideoCapture("../../vtest.avi")
	if not capture.isOpened():
		print("Unable to open video file")
		exit(0)
	#TODO:
	# Generate side-by-side video of FG mask and video
	#width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
	
	while True:
		ret, frame = capture.read()
		if frame is None:
			break
		fgMask = backSub.apply(frame)
		cv.rectangle(frame, (10,2), (100,20), (255,255,255), cv.FILLED)
		cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15,15), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0))
		cv.imshow("Frame", frame)
		cv.imshow("FG Mask", fgMask)

		keyboard = cv.waitKey(30)
		if keyboard == ord('q') or keyboard == 27:
			break

if __name__ == "__main__":
	background_removal(algo) # This is just to test this thing out