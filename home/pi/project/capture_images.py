import numpy as np
import time
import sys

# ...

def read_camera_intrinsics(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        intrinsics = {}
        for line in lines:
            if line.startswith('#'):
                continue
            key, value = line.split(':')
            intrinsics[key.strip()] = float(value.strip())
    return intrinsics

# ...

# Read camera intrinsics
intrinsics_path = '/home/pi/project/camera_intrinsics/camera_intrinsics.txt'
camera_intrinsics = read_camera_intrinsics(intrinsics_path)

# Use the camera intrinsics in the depth map computation
# ...



def start_recording(duration):
    # Start capturing images and computing depth maps
    start_time = time.time()
    while time.time() - start_time < duration:
        # Capture images and compute depth maps
        # ...

    # Transfer depth maps to Raspberry Pi 2
    # ...

def stop_recording():
    # Stop capturing images and computing depth maps
    # ...

# Main program
if len(sys.argv) > 1:
    duration = int(sys.argv[1])
    start_recording(duration)
else:
    stop_recording()


#####Add in below:

import cv2
import numpy as np
import os
import yaml
import time
import subprocess

# Load camera calibration data
with open('camera_calibration.yaml', 'r') as file:
    calibration_data = yaml.safe_load(file)

# Extract calibration parameters
left_camera_matrix = np.array(calibration_data['left_camera_matrix'])
left_distortion_coeffs = np.array(calibration_data['left_distortion_coeffs'])
right_camera_matrix = np.array(calibration_data['right_camera_matrix'])
right_distortion_coeffs = np.array(calibration_data['right_distortion_coeffs'])
stereo_rotation = np.array(calibration_data['stereo_rotation'])
stereo_translation = np.array(calibration_data['stereo_translation'])

# Set up stereo camera configuration
stereo_config = cv2.stereoBM_create()
stereo_config.setNumDisparities(128)
stereo_config.setBlockSize(15)

def capture_images():
    left_camera = cv2.VideoCapture(0)  # Adjust the camera index if necessary
    right_camera = cv2.VideoCapture(1)  # Adjust the camera index if necessary

    while True:
        # Capture images from left and right cameras
        ret_left, left_frame = left_camera.read()
        ret_right, right_frame = right_camera.read()

        if ret_left and ret_right:
            # Undistort the images using camera calibration data
            left_undistorted = cv2.undistort(left_frame, left_camera_matrix, left_distortion_coeffs)
            right_undistorted = cv2.undistort(right_frame, right_camera_matrix, right_distortion_coeffs)

            # Compute depth map
            disparity = stereo_config.compute(cv2.cvtColor(left_undistorted, cv2.COLOR_BGR2GRAY),
                                              cv2.cvtColor(right_undistorted, cv2.COLOR_BGR2GRAY))
            depth_map = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

            # Save depth map to a file
            timestamp = int(time.time())
            depth_map_filename = f'depth_map_{timestamp}.png'
            cv2.imwrite(depth_map_filename, depth_map)

            # Transfer depth map to Raspberry Pi 2
            subprocess.run(['scp', depth_map_filename, 'pi@raspberrypi2:/path/to/depth_maps/'])

            # Remove the depth map file after transfer
            os.remove(depth_map_filename)

        else:
            break

    left_camera.release()
    right_camera.release()

def start_recording(duration):
    start_time = time.time()

    while time.time() - start_time < duration:
        capture_images()

    print('Recording completed.')

def stop_recording():
    print('Recording stopped.')

# Check command-line arguments
if len(sys.argv) > 1:
    duration = int(sys.argv[1])
    start_recording(duration)
else:
    stop_recording()
