import numpy as np
import time
import sys
import cv2
import numpy as np
import os
import yaml
import time
import subprocess

# Load camera calibration data
with open('camera_calibration.yaml', 'r') as file:
    calibration_data = yaml.safe_load(file)

# Extract calibration parameters for each camera
camera_params = calibration_data['camera_params']

def capture_images():
    cameras = []
    for i in range(4):
        camera = cv2.VideoCapture(i)
        cameras.append(camera)

    while True:
        frames = []
        for camera in cameras:
            ret, frame = camera.read()
            if ret:
                frames.append(frame)

        if len(frames) == 4:
            # Perform depth map computation using the frames from all cameras
            # ...

            # Save depth map to a file
            timestamp = int(time.time())
            depth_map_filename = f'depth_map_{timestamp}.png'
            cv2.imwrite(depth_map_filename, depth_map)

            # Transfer depth map to Raspberry Pi 2
            subprocess.run(['scp', depth_map_filename, 'pi@raspberrypi2:/path/to/depth_maps/'])

            # Remove the depth map file after transfer
            os.remove(depth_map_filename)

    for camera in cameras:
        camera.release()



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


# Main program
if len(sys.argv) > 1:
    duration = int(sys.argv[1])
    start_recording(duration)
else:
    stop_recording()


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
    cameras = []
    for i in range(4):
        camera = cv2.VideoCapture(i)
        cameras.append(camera)

    frame_count = 0
    while True:
        frames = []
        for camera in cameras:
            ret, frame = camera.read()
            if ret:
                frames.append(frame)

        if len(frames) == 4:
            # Save the captured frames as JPEG images
            for i, frame in enumerate(frames):
                frame_filename = f'frame{i+1}_{frame_count}.jpg'
                cv2.imwrite(frame_filename, frame)

            # Perform depth map computation using the frames from all cameras
            # ...

            # Save depth map to a file
            timestamp = int(time.time())
            depth_map_filename = f'depth_map_{timestamp}.png'
            cv2.imwrite(depth_map_filename, depth_map)

            # Transfer depth map to Raspberry Pi 2
            subprocess.run(['scp', depth_map_filename, 'pi@raspberrypi2:/path/to/depth_maps/'])

            # Remove the depth map file after transfer
            os.remove(depth_map_filename)

            frame_count += 1

    for camera in cameras:
        camera.release()

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
