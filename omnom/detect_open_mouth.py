
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

class MahMouth():

	# define one constants, for mouth aspect ratio to indicate open mouth
	MOUTH_AR_THRESH = 0.79
	# grab the indexes of the facial landmarks for the mouth
	(mStart, mEnd) = (49, 68)
	(bStart, bEnd) = (18,27)
	(eStart, eEnd) = (37, 48)

	def __init__(self):
		self.construct_arguments()
		self.detector_predictor()
		self.start_camera()

	def __del__(self):
		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()

	def construct_arguments(self):
			# construct the argument parse and parse the arguments
		self.ap = argparse.ArgumentParser()
		self.ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
			help="path to facial landmark predictor")
		self.ap.add_argument("-w", "--webcam", type=int, default=0,
			help="index of webcam on system")
		self.args = vars(self.ap.parse_args())

	def detector_predictor(self):
		# initialize dlib's face detector (HOG-based) and then create
		# the facial landmark predictor
		print("[INFO] loading facial landmark predictor...")
		self.detector = dlib.get_frontal_face_detector()
		self.predictor = dlib.shape_predictor(self.args["shape_predictor"])

	def start_camera(self):
			# start the video stream thread
		print("[INFO] starting video stream thread...")
		self.vs = VideoStream(src=self.args["webcam"]).start()

		time.sleep(1.0)	

	def mouth_aspect_ratio(self, mouth):
		# compute the euclidean distances between the two sets of
		# vertical mouth landmarks (x, y)-coordinates
		A = dist.euclidean(mouth[2], mouth[10]) # 51, 59
		B = dist.euclidean(mouth[4], mouth[8]) # 53, 57
		# compute the euclidean distance between the horizontal
		# mouth landmark (x, y)-coordinates
		C = dist.euclidean(mouth[0], mouth[6]) # 49, 55

		# compute the mouth aspect ratio
		mar = (A + B) / (2.0 * C)

		# return the mouth aspect ratio
		return mar

	def brow_movement(self, brows, eyes):
		left = dist.euclidean(brows[3], eyes[2]) # 21, 39
		right = dist.euclidean(brows[6], eyes[7]) # 24, 44
		eye_dist = dist.euclidean(eyes[3], eyes[6]) #40, 43

		diff = (left + right) / (2.0 * eye_dist)
		if diff > 0.5:
			reset = True
		else:
			reset = False

		print(reset)
		return reset

	def update(self):

		frame = self.vs.read()
		frame = imutils.resize(frame, width=640)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# detect faces in the grayscale frame
		rects = self.detector(gray, 0)

		# loop over the face detections
		for rect in rects:
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy array
			shape = self.predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)

			# extract the mouth coordinates, then use the
			# coordinates to compute the mouth aspect ratio
			mouth = shape[self.mStart:self.mEnd]
			brows = shape[self.bStart:self.bEnd]
			eyes = shape[self.eStart:self.eEnd]

			mouthAR = self.mouth_aspect_ratio(mouth)
			browsAR = self.brow_movement(brows, eyes)

			right_eye = shape[37:42]
			left_eye = shape[43:46]

			# compute the convex hull for the mouth, then
			# visualize the mouth
			mouthHull = cv2.convexHull(mouth)
			left_eyeHull = cv2.convexHull(left_eye)
			right_eyeHull = cv2.convexHull(right_eye)
			
			#cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 2)
			#cv2.drawContours(frame, [left_eyeHull], -1, (0, 255, 0), 1)
			#cv2.drawContours(frame, [right_eyeHull], -1, (0, 255, 0), 1)
			cv2.putText(frame, "MAR: {:.2f}".format(mouthAR), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

			for (x, y) in shape:
				cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

			# Draw text if mouth is open
			if mouthAR > mouthcheck.MOUTH_AR_THRESH:
				isopen = True
				cv2.putText(frame, "Mouth is Open!", (30,60),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
			else:
				isopen = False
				
					# Draw text if mouth is open
			if browsMOVED == True:
				cv2.putText(frame, "Reset!", (30,90),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)

		# show the frame
		cv2.imshow("Frame", frame)

		return isopen

if __name__ == "__main__":
	mouthcheck = MahMouth()

	while True:
		mouthopen = mouthcheck.update()
		#print(mouthopen)
		# if the `q` key was pressed, break from the loop
		key = cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break