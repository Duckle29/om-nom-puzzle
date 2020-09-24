
import os
import subprocess
import platform
import glob
import tobii_research as tr
import time


def init_eyetracker():
    """ Findes the eyetracker and returns it

    Returns:
        [type]: returns eyetracker
    """
    found_eyetrackers = tr.find_all_eyetrackers()
    my_eyetracker = found_eyetrackers[0]
    print("Address: " + my_eyetracker.address)
    print("Model: " + my_eyetracker.model)
    print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
    print("Serial number: " + my_eyetracker.serial_number)
    return my_eyetracker

def gaze_data_callback(gaze_data):
    # Print gaze points of left and right eye
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

def call_eyetracker_manager(my_eyetracker, manager_mode):
    if manager_mode == 0:
        mode = "usercalibration"
    elif manager_mode == 1:
        mode = "displayarea"
    else:
        print("mode not supported...")
        exit(1)

    try:
        os_type = platform.system()
        ETM_PATH = ''
        DEVICE_ADDRESS = ''
        if os_type == "Windows":
            ETM_PATH = glob.glob(os.environ["LocalAppData"] +
                                 "/Programs/TobiiProEyeTrackerManager/TobiiProEyeTrackerManager.exe")[0]
            DEVICE_ADDRESS = my_eyetracker.address
        elif os_type == "Linux":
            ETM_PATH = "TobiiProEyeTrackerManager"
            DEVICE_ADDRESS = "tobii-ttp://TOBII-IS404-100107417574"
        elif os_type == "Darwin":
            ETM_PATH = "/Applications/TobiiProEyeTrackerManager.app/Contents/MacOS/TobiiProEyeTrackerManager"
            DEVICE_ADDRESS = "tobii-ttp://TOBII-IS404-100107417574"
        else:
            print("Unsupported...")
            exit(1)

        eyetracker = tr.EyeTracker(DEVICE_ADDRESS)

        #mode = "usercalibration" #"displayarea"

        etm_p = subprocess.Popen([ETM_PATH,
                                  "--device-address=" + eyetracker.address,
                                  "--mode=" + mode],
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


if __name__ == "__main__":
    my_eyetracker = init_eyetracker()

    call_eyetracker_manager(my_eyetracker, 0)
    call_eyetracker_manager(my_eyetracker, 1)

    #my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
    #time.sleep(5)
    #my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)