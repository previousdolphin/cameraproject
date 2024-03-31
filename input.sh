#!/bin/bash

# Define the IP addresses of the Raspberry Pis
PI1_IP="192.168.0.1"  # Replace with the IP address of the first Raspberry Pi
PI2_IP="192.168.0.2"  # Replace with the IP address of the second Raspberry Pi

# Define the file paths on the Raspberry Pis
PI1_SCRIPT_PATH="/home/pi/project/capture_images.py"
PI1_DEPTH_PATH="/home/pi/project/depth_maps"
PI1_INTRINSICS_PATH="/home/pi/project/camera_intrinsics"

PI2_SCRIPT_PATH="/home/pi/project/create_3d_model.py"
PI2_IMAGES_PATH="/home/pi/project/images"
PI2_DEPTH_PATH="/home/pi/project/depth_maps"
PI2_INTRINSICS_PATH="/home/pi/project/camera_intrinsics"
PI2_OUTPUT_PATH="/home/pi/project/output"

# Create the necessary directories on the Raspberry Pis
ssh pi@$PI1_IP "mkdir -p $PI1_DEPTH_PATH $PI1_INTRINSICS_PATH"
ssh pi@$PI2_IP "mkdir -p $PI2_IMAGES_PATH $PI2_DEPTH_PATH $PI2_INTRINSICS_PATH $PI2_OUTPUT_PATH"


# Copy the camera intrinsic matrices to the Raspberry Pis
scp camera_intrinsics.txt pi@$PI1_IP:$PI1_INTRINSICS_PATH/
scp camera_intrinsics.txt pi@$PI2_IP:$PI2_INTRINSICS_PATH/

# Start the image capture and depth map computation on the first Raspberry Pi
ssh pi@$PI1_IP "python $PI1_SCRIPT_PATH"

# Transfer the captured images and depth maps from the first Raspberry Pi to the second Raspberry Pi
ssh pi@$PI1_IP "rsync -avz $PI1_DEPTH_PATH/ pi@$PI2_IP:$PI2_DEPTH_PATH/"

# Start the 3D model creation on the second Raspberry Pi
ssh pi@$PI2_IP "python $PI2_SCRIPT_PATH"

# Retrieve the generated 3D model from the second Raspberry Pi
scp pi@$PI2_IP:$PI2_OUTPUT_PATH/output_3d_model.obj ./
