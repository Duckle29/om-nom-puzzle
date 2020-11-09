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
    MOUTH_AR_THRESH = 0.79
    # grab the indexes of the facial landmarks for the mouth
    (mStart, mEnd) = (49, 68)

    def __init__(self):
        self.construct_arguments()
        self.detector_predictor()
        self.start_camera()
        self.isopen = True

    def __del__(self):
        # do a bit of cleanup
        cv2.destroyAllWindows()
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

    def update(self):

        frame = self.vs.read()
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces in the grayscale frame
        rects = self.detector(gray, 0)
        print(rects)

        # loop over the face detections
        for rect in rects:
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy array
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

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
            if mar > mouthcheck.MOUTH_AR_THRESH:
                self.isopen = True
                cv2.putText(
                    frame, "Mouth is Open!", (30, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                self.isopen = False

        # show the frame
        cv2.imshow("Frame", frame)

        return self.isopen

if __name__ == "__main__":
    mouthcheck = MahMouth()

    while True:
        mouthopen = mouthcheck.update()
        print(mouthopen)
        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
