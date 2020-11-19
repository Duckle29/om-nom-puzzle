import time

from scipy.spatial import distance as dist
import imutils
from imutils.video import VideoStream, WebcamVideoStream
from imutils import face_utils
import argparse
import dlib
import cv2


class MahMouth():

    # define one constants, for mouth aspect ratio to indicate open mouth
<<<<<<< HEAD
    MOUTH_AR_THRESH = 0.79
    # grab the indexes of the facial landmarks for the mouth
    (mStart, mEnd) = (49, 68)
=======
    MOUTH_AR_THRESH = 0.65
    BROWS_AR_THRESH = 0.70
    # grab the indexes of the facial landmarks for the mouth
    (mStart, mEnd) = (48, 67)
    (bStart, bEnd) = (17,26)
    (eStart, eEnd) = (36, 47)
>>>>>>> origin/mouthopen

    def __init__(self):
        self.construct_arguments()
        self.detector_predictor()
        self.start_camera()
<<<<<<< HEAD
        self.isopen = True
=======
        self.mouthopen = True
        self.browsup = False
>>>>>>> origin/mouthopen

    def __del__(self):
        # do a bit of cleanup
        cv2.destroyAllWindows()
<<<<<<< HEAD
        self.vs.stop()

    def mouth_aspect_ratio(self, mouth):
        # compute the euclidean distances between the two sets of
        # vertical mouth landmarks (x, y)-coordinates
        A = dist.euclidean(mouth[2], mouth[10])  # 51, 59
        B = dist.euclidean(mouth[4], mouth[8])  # 53, 57
        # compute the euclidean distance between the horizontal
        # mouth landmark (x, y)-coordinates
        C = dist.euclidean(mouth[0], mouth[6])  # 49, 55

        # compute the mouth aspect ratio
        mar = (A + B) / (2.0 * C)

        # return the mouth aspect ratio
        return mar

    def construct_arguments(self):
        # construct the argument parse and parse the arguments
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument(
            "-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
            help="path to facial landmark predictor")
        self.ap.add_argument(
            "-w", "--webcam", type=int, default=0,
=======
        vs.stop()

    def construct_arguments(self):
            # construct the argument parse and parse the arguments
        self.ap = argparse.ArgumentParser()
        self.ap.add_argument("-p", "--shape-predictor", required=False, default='shape_predictor_68_face_landmarks.dat',
            help="path to facial landmark predictor")
        self.ap.add_argument("-w", "--webcam", type=int, default=0,
>>>>>>> origin/mouthopen
            help="index of webcam on system")
        self.args = vars(self.ap.parse_args())

    def detector_predictor(self):
        # initialize dlib's face detector (HOG-based) and then create
        # the facial landmark predictor
        print("[INFO] loading facial landmark predictor...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.args["shape_predictor"])

    def start_camera(self):
<<<<<<< HEAD
        # start the video stream thread
        print("[INFO] starting video stream thread...")
        self.vs = VideoStream(src=self.args["webcam"]).start()

        time.sleep(1.0)
=======
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
        return diff
>>>>>>> origin/mouthopen

    def update(self):

        frame = self.vs.read()
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)
<<<<<<< HEAD
        print(rects)
=======
>>>>>>> origin/mouthopen

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

<<<<<<< HEAD
            # extract the mouth coordinates, then use the
            # coordinates to compute the mouth aspect ratio
            mouth = shape[self.mStart:self.mEnd]

            mouthMAR = self.mouth_aspect_ratio(mouth)
            mar = mouthMAR
            # compute the convex hull for the mouth, then
            # visualize the mouth
            mouthHull = cv2.convexHull(mouth)

            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 2)
            cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Draw text if mouth is open
            if mar > self.MOUTH_AR_THRESH:
                self.isopen = True
                cv2.putText(
                    frame, "Mouth is Open!", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                self.isopen = False

        # show the frame
        #cv2.imshow("Frame", frame)

        return self.isopen
=======
            (x, y, w, h) = cv2.boundingRect(np.array(shape))
            #frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255,0,0), 2)

            roi = frame[y:y + h, x:x + w]
            roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)
            cv2.imshow("ROI", roi)

            # extract the mouth coordinates, then use the
            # coordinates to compute the mouth aspect ratio
            mouth = shape[self.mStart:self.mEnd]
            brows = shape[self.bStart:self.bEnd]
            eyes = shape[self.eStart:self.eEnd]

            mouthAR = self.mouth_aspect_ratio(mouth)
            browsAR = self.brow_movement(brows, eyes)

            right_eye = shape[42:47]
            left_eye = shape[36:41]

            # compute the convex hull for the mouth, then
            # visualize the mouth
            mouthHull = cv2.convexHull(mouth)
            left_eyeHull = cv2.convexHull(left_eye)
            right_eyeHull = cv2.convexHull(right_eye)
            
            # Draw outline of hulls
            cv2.drawContours(frame, [mouthHull], -1, (0, 255, 0), 2)
            cv2.drawContours(frame, [left_eyeHull], -1, (0, 255, 0), 2)
            cv2.drawContours(frame, [right_eyeHull], -1, (0, 255, 0), 2)

            # Write ratios to screen
            #cv2.putText(frame, "Mouth AR: {:.2f}".format(mouthAR), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #cv2.putText(frame, "Brows AR: {:.2f}".format(browsAR), (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Draw landmarks
            #for (x, y) in shape:
            #	cv2.circle(frame, (x, y), 1, (0, 255, 0), -1)

            # Draw distances
            cv2.line(frame, (left_eye[3][0], left_eye[3][1]), (right_eye[0][0], right_eye[0][1]), (0,0,255), 2)
            cv2.line(frame, (brows[3][0], brows[3][1]), (left_eye[2][0], left_eye[2][1]), (255,0,0), 2)
            cv2.line(frame, (brows[6][0], brows[6][1]), (right_eye[1][0], right_eye[1][1]), (255,0,0), 2)
            cv2.line(frame, (mouth[2][0], mouth[2][1]), (mouth[10][0], mouth[10][1]), (255,0,0), 2)
            cv2.line(frame, (mouth[4][0], mouth[4][1]), (mouth[8][0], mouth[8][1]), (255,0,0), 2)
            cv2.line(frame, (mouth[0][0], mouth[0][1]), (mouth[6][0], mouth[6][1]), (0,0,255), 2)

            # Draw text if mouth is open
            if mouthAR > mouthcheck.MOUTH_AR_THRESH:
                self.mouthopen = True
                cv2.putText(frame, "Mouth is Open!", (30,60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            else:
                self.mouthopen = False
                
            # Draw text if brows are raised
            if browsAR > mouthcheck.BROWS_AR_THRESH:
                self.browsup = True
                cv2.putText(frame, "Reset!", (30,90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255),2)
            else:
                self.browsup = False

        # show the frame
        cv2.imshow("Frame", frame)
        return self.mouthopen, self.browsup
>>>>>>> origin/mouthopen

if __name__ == "__main__":
    mouthcheck = MahMouth()

    while True:
<<<<<<< HEAD
        mouthopen = mouthcheck.update()
        print(mouthopen)
        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
=======
        mouthopen, browsup = mouthcheck.update()
        #print(mouthopen)
        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
>>>>>>> origin/mouthopen
