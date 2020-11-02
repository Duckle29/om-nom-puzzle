
import os
import subprocess
import platform
import glob
import tobii_research as tr
import time
import collections
import math

class MahEye():
    pos = {"left": collections.deque(maxlen=10), "right":collections.deque(maxlen=10)}
    eyetracker = None

    def init_eyetracker(self):
        """ Findes the eyetracker and returns it

        Returns:
            [type]: returns eyetracker
        """
        found_eyetrackers = tr.find_all_eyetrackers()
        self.eyetracker = found_eyetrackers[0]
        print(f"""Address: {self.eyetracker.address}
        Model: {self.eyetracker.model}
        Name: {self.eyetracker.device_name}
        S/N: {self.eyetracker.serial_number}""")

    def gaze_data_callback(self, gaze_data):
        self.pos['left'].append(gaze_data['left_gaze_point_on_display_area'])
        self.pos['right'].append(gaze_data['right_gaze_point_on_display_area'])

    def call_eyetracker_manager(self):

        try:
            os_type = platform.system()
            ETM_PATH = ''
            DEVICE_ADDRESS = ''
            if os_type == "Windows":
                ETM_PATH = glob.glob(os.environ["LocalAppData"] +
                                    "/Programs/TobiiProEyeTrackerManager/TobiiProEyeTrackerManager.exe")[0]
                DEVICE_ADDRESS = self.eyetracker.address
            elif os_type == "Linux":
                ETM_PATH = "TobiiProEyeTrackerManager"
                DEVICE_ADDRESS = "tobii-ttp://TOBII-IS404-100107417574"
            else:
                print("Unsupported...")
                exit(1)

            etm_p = subprocess.Popen([ETM_PATH,
                                    "--device-address=" + self.eyetracker.address],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=False)

            stdout, stderr = etm_p.communicate()  # Returns a tuple with (stdout, stderr)

            if etm_p.returncode == 0:
                print("Eye Tracker Manager was called successfully!")
            else:
                print("Eye Tracker Manager call returned the error code: " + str(etm_p.returncode))
                errlog = None
                if os_type == "Windows":
                    errlog = stdout  # On Windows ETM error messages are logged to stdout
                else:
                    errlog = stderr

                for line in errlog.splitlines():
                    if line.startswith("ETM Error:"):
                        print(line)

        except Exception as e:
            print(e)

    def start_eyetracker(self):
        self.eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback, as_dictionary=True)

    def stop_eyetracker(self):
        self.eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, self.gaze_data_callback)

    def get_pos(self):
        pos_sums = [0, 0]
        counts = len(self.pos['left'])
        for p in self.pos['left']:
            if math.isnan(p[0]) or math.isnan(p[1]):
                counts -= 1
                continue
            pos_sums[0] += p[0]
            pos_sums[1] += p[1]

        if counts == 0:
            left_avg = None
        else:
            left_avg = [pos_sums[0]/ len(self.pos['left']), pos_sums[1]/ len(self.pos['left'])]

        pos_sums = [0, 0]
        counts = len(self.pos['right'])
        for p in self.pos['right']:
            if math.isnan(p[0]) or math.isnan(p[1]):
                counts -= 1
                continue
            pos_sums[0] += p[0]
            pos_sums[1] += p[1]

        if counts == 0:
            right_avg = None
        else:
            right_avg = [pos_sums[0]/ len(self.pos['right']), pos_sums[1]/ len(self.pos['right'])]

        if right_avg is None or left_avg is None:
            return None

        return [(left_avg[0]+right_avg[0])/2, (left_avg[1]+right_avg[1])/2]

    def __init__(self):
        self.init_eyetracker()
        self.call_eyetracker_manager()
        self.start_eyetracker()

    def __del__(self):
        self.stop_eyetracker()

if __name__ == "__main__":

    eyetracker = mah_eye()

    while True:
        time.sleep(1)
        print(eyetracker.get_pos())
    #time.sleep(2)

    eyetracker.stop_eyetracker()