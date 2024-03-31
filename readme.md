# 3D Capture System with Helmet-Mounted Cameras

This project implements a 3D capture system using helmet-mounted cameras and Raspberry Pi devices. The system captures images from multiple cameras, computes depth maps, and generates a 3D model of the surrounding environment.

## Project Hierarchy

```
├── raspberry_pi_1/
│   ├── capture_images.py
│   ├── start_recording.sh
│   ├── stop_recording.sh
│   └── camera_calibration.yaml
├── raspberry_pi_2/
│   ├── create_3d_model.py
│   └── config.yaml
├── networked_computer/
│   ├── control_script.py
│   └── diagnostic_logger.py
└── README.md
```

## File Descriptions

### Raspberry Pi 1

- `capture_images.py`: This script runs on Raspberry Pi 1 and is responsible for capturing images from multiple cameras, computing depth maps, and transferring the depth maps to Raspberry Pi 2. It accepts the recording duration as a command-line argument.

- `start_recording.sh`: This shell script is used to start the image capture and depth map computation process on Raspberry Pi 1. It calls the `capture_images.py` script with the specified recording duration.

- `stop_recording.sh`: This shell script is used to stop the image capture and depth map computation process on Raspberry Pi 1. It terminates the `capture_images.py` script.

- `camera_calibration.yaml`: This file contains the camera calibration parameters required for accurate depth map computation. It includes the intrinsic and extrinsic parameters for each camera.

### Raspberry Pi 2

- `create_3d_model.py`: This script runs on Raspberry Pi 2 and is responsible for receiving depth maps from Raspberry Pi 1, creating a 3D model using the depth information, and saving the generated model. It continuously monitors the depth map folder for new depth maps and creates updated 3D models whenever new depth maps are available.

- `config.yaml`: This file contains the configuration parameters for the 3D capture system, such as the paths for depth map storage and 3D model output, and the intrinsic camera parameters.

### Networked Computer

- `control_script.py`: This script runs on the networked computer and acts as the main control interface for starting and stopping the recording session, and retrieving the generated 3D model. It communicates with the Raspberry Pis using SSH and sends commands to control the recording process.

- `diagnostic_logger.py`: This script provides diagnostic logging and system monitoring capabilities. It captures information such as CPU usage, memory usage, disk usage, and performance metrics for various operations like image capture, depth map computation, and 3D model creation. The logged data is stored in a file named `diagnostic.log`.

## Setup and Usage

1. Connect the cameras to Raspberry Pi 1 and ensure proper connectivity.
2. Set up the network communication between Raspberry Pi 1, Raspberry Pi 2, and the networked computer.
3. Perform camera calibration and update the `camera_calibration.yaml` file with the obtained parameters.
4. Configure the `config.yaml` file with the appropriate paths and intrinsic camera parameters.
5. Install the required dependencies on each device (OpenCV, Open3D, NumPy, PyYAML, Paramiko, psutil).
6. Run the `control_script.py` on the networked computer to start and control the recording session.
7. Monitor the diagnostic information logged in the `diagnostic.log` file for system health and performance analysis.

Please refer to the individual scripts and configuration files for more detailed information on their usage and functionalities.

## Troubleshooting

If you encounter any issues or errors during the setup or execution of the project, please refer to the troubleshooting guide in the project documentation. If the problem persists, feel free to open an issue on the project repository or contact the project maintainer for assistance.

## License

This project is licensed under the [MIT License](LICENSE).
