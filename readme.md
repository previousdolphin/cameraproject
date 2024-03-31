Project Overview:

The goal of this project is to create a 360-degree video stitching and streaming system using two Raspberry Pi devices, each equipped with four cameras. The stitched video will be accessible from another computer via a network connection.

System Architecture:

1\. Raspberry Pi 1:

 - Connected to 4 cameras (Camera 1, Camera 2, Camera 3, Camera 4)

 - Captures video frames from the cameras

 - Performs video stitching to create a partial equirectangular frame

 - Sends the partial equirectangular frame to Raspberry Pi 2 over the network

2\. Raspberry Pi 2:

 - Connected to 4 cameras (Camera 5, Camera 6, Camera 7, Camera 8)

 - Captures video frames from the cameras

 - Performs video stitching to create a partial equirectangular frame

 - Receives the partial equirectangular frame from Raspberry Pi 1

 - Combines the partial equirectangular frames from both Raspberry Pis to create a complete equirectangular frame

 - Runs an RTSP server to stream the stitched video

 - Hosts a Flask server to serve the video feed via HTTP

3\. Client Computer:

 - Connects to Raspberry Pi 2 over the network

 - Accesses the video stream via RTSP using a media player (e.g., VLC)

 - Accesses the video feed via HTTP using a web browser

Code Distribution:

1\. Raspberry Pi 1:

 - `camera_capture.py`: Code to capture video frames from the connected cameras

 - `video_stitching.py`: Code to perform video stitching and create a partial equirectangular frame

 - `network_communication.py`: Code to send the partial equirectangular frame to Raspberry Pi 2 over the network

2\. Raspberry Pi 2:

 - `camera_capture.py`: Code to capture video frames from the connected cameras

 - `video_stitching.py`: Code to perform video stitching and create a partial equirectangular frame

 - `network_communication.py`: Code to receive the partial equirectangular frame from Raspberry Pi 1

 - `video_combining.py`: Code to combine the partial equirectangular frames from both Raspberry Pis

 - `rtsp_server.py`: Code to run the RTSP server and stream the stitched video

 - `flask_server.py`: Code to host the Flask server and serve the video feed via HTTP

 - `compass_overlay.py`: Code to generate and overlay the compass on the stitched video

Project Plan:

1\. Set up the hardware:

 - Connect 4 cameras to each Raspberry Pi

 - Ensure proper power supply and network connectivity for both Raspberry Pis

2\. Develop and test the code:

 - Implement `camera_capture.py` on both Raspberry Pis to capture video frames from the cameras

 - Implement `video_stitching.py` on both Raspberry Pis to perform video stitching and create partial equirectangular frames

 - Implement `network_communication.py` on both Raspberry Pis to establish communication and transfer partial equirectangular frames

 - Implement `video_combining.py` on Raspberry Pi 2 to combine the partial equirectangular frames into a complete frame

 - Implement `rtsp_server.py` and `flask_server.py` on Raspberry Pi 2 to stream and serve the stitched video

 - Implement `compass_overlay.py` on Raspberry Pi 2 to generate and overlay the compass on the stitched video

3\. Integration and testing:

 - Combine all the components and test the end-to-end functionality

 - Verify the video stitching quality and performance

 - Test the video streaming and accessibility from the client computer

4\. Optimization and refinement:

 - Optimize the code for better performance and resource utilization

 - Fine-tune the video stitching algorithms and parameters

 - Enhance the user experience by adding controls and features on the client side

5\. Deployment and documentation:

 - Deploy the system in the target environment

 - Prepare user documentation and guidelines for setting up and using the system

 - Provide troubleshooting and maintenance instructions


Here's how the scripts works:

1\. The script starts by executing the processes on Raspberry Pi 1.

2\. It runs `camera_capture.py`, `video_stitching.py`, and `network_communication.py` in the background using the `&` operator. This allows the script to continue executing without waiting for each process to finish.

3\. After starting the processes on Raspberry Pi 1, the script moves on to Raspberry Pi 2.

4\. On Raspberry Pi 2, it runs `camera_capture.py`, `video_stitching.py`, `video_combining.py`, `rtsp_server.py`, `flask_server.py`, and `compass_overlay.py` in the background.

5\. Finally, the script prints a message indicating that all processes have started successfully.

To use this script:

1\. Create a new file with a `.sh` extension (e.g., `startup_script.sh`) on both Raspberry Pi devices.

2\. Copy the script code into the file on each Raspberry Pi.

3\. Make the script executable by running the following command on both Raspberry Pi devices:

   ```

   chmod +x startup_script.sh

   ```

4\. Run the script on Raspberry Pi 1 by executing the following command:

   ```

   ./startup_script.sh

   ```

5\. Run the script on Raspberry Pi 2 by executing the same command:

   ```

   ./startup_script.sh

   ```

The script will start all the necessary processes on both Raspberry Pi devices in the correct order. The processes will run in the background, allowing the script to complete execution while the processes continue running.

Note: Make sure that you have the necessary Python files (`camera_capture.py`, `video_stitching.py`, `network_communication.py`, `video_combining.py`, `rtsp_server.py`, `flask_server.py`, and `compass_overlay.py`) in the same directory as the shell script on each Raspberry Pi.

If you want to stop the processes later, you can use the `pkill` command followed by the process name (e.g., `pkill -f camera_capture.py`) on each Raspberry Pi.
