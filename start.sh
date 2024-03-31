#!/bin/bash

# Raspberry Pi 1
echo "Starting processes on Raspberry Pi 1..."

# Start camera capture
python3 camera_capture.py &

# Start video stitching
python3 video_stitching.py &

# Start network communication
python3 network_communication.py &

# Raspberry Pi 2
echo "Starting processes on Raspberry Pi 2..."

# Start camera capture
python3 camera_capture.py &

# Start video stitching
python3 video_stitching.py &

# Start video combining
python3 video_combining.py &

# Start RTSP server
python3 rtsp_server.py &

# Start Flask server
python3 flask_server.py &

# Start compass overlay
python3 compass_overlay.py &

echo "All processes started successfully!"
