# 3D Capture System with Helmet-Mounted Cameras

This project implements a 3D capture system using helmet-mounted cameras and Raspberry Pi devices. The system captures images from multiple cameras, computes depth maps, generates 3D models, and provides a web-based interface for monitoring and controlling the process.

## Project Overview

The 3D capture system consists of the following components:

- Raspberry Pi 1: Captures images from multiple cameras and computes depth maps.
- Raspberry Pi 2: Receives depth maps from Raspberry Pi 1 and creates 3D models.
- Control Computer: Runs a Flask server to control and monitor the system.

The control computer communicates with the Raspberry Pis via SSH to start and monitor the image capture and 3D modeling processes. The Flask server provides a web-based interface for user interaction and displays diagnostic information.

## Hardware Requirements

- 2 Raspberry Pi devices (Raspberry Pi 1 and Raspberry Pi 2)
- Multiple cameras compatible with Raspberry Pi
- Helmet or suitable mounting apparatus for the cameras
- Control computer (laptop or desktop)
- Ethernet switch or Wi-Fi router for network connectivity
- Power supply for the Raspberry Pis (e.g., Waveshare UPS with 15000mAh battery)

## Software Requirements

- Raspberry Pi OS (installed on both Raspberry Pis)
- Python 3.x (installed on Raspberry Pis and control computer)
- OpenCV library (installed on Raspberry Pis)
- Flask framework (installed on control computer)
- Paramiko library (installed on control computer)
- Other project dependencies (listed in requirements.txt)

## Project Structure

```
├── raspberry_pi_1/
│   ├── capture_images.py
│   └── diagnostic_logger.py
├── raspberry_pi_2/
│   ├── create_3d_model.py
│   └── diagnostic_logger.py
├── control_computer/
│   ├── flask_server.py
│   ├── templates/
│   │   ├── index.html
│   │   └── diagnostics.html
│   └── static/
│       └── style.css
├── requirements.txt
└── README.md
```

## Setup and Installation

1. Set up the hardware components:
   - Connect the cameras to Raspberry Pi 1.
   - Configure the network connectivity between the Raspberry Pis and the control computer.
   - Mount the cameras on the helmet or suitable apparatus.

2. Install the required software:
   - Install Raspberry Pi OS on both Raspberry Pis.
   - Install Python 3.x on the Raspberry Pis and the control computer.
   - Install the necessary libraries and dependencies on the Raspberry Pis and the control computer.

3. Clone the project repository on the control computer and the Raspberry Pis.

4. Configure the project:
   - Update the SSH connection details in `flask_server.py` with the appropriate IP addresses, usernames, and passwords for the Raspberry Pis.
   - Modify any other configuration settings as needed.

5. Start the system:
   - Run the Flask server on the control computer: `python flask_server.py`.
   - Access the web-based interface by opening a web browser and navigating to `http://<control_computer_ip>:5000`.
   - Use the interface to start the image capture and 3D modeling processes on the Raspberry Pis.

## Usage

1. Power on the Raspberry Pis and ensure they are connected to the network.

2. Start the Flask server on the control computer:
   ```
   python flask_server.py
   ```

3. Open a web browser and navigate to `http://<control_computer_ip>:5000` to access the web-based interface.

4. Use the provided buttons or links to start the image capture process on Raspberry Pi 1 and the 3D modeling process on Raspberry Pi 2.

5. Monitor the progress and diagnostic information displayed on the web interface.

6. The captured images and generated 3D models will be stored on the respective Raspberry Pis.

7. To stop the system, press `Ctrl+C` in the terminal where the Flask server is running.

## Troubleshooting

- If the web interface is not accessible, check the network connectivity and ensure that the Flask server is running on the control computer.
- If the image capture or 3D modeling processes do not start, verify the SSH connection details in `flask_server.py` and ensure that the Raspberry Pis are properly set up.
- Check the diagnostic logs on the Raspberry Pis and the control computer for any error messages or warnings.
- Ensure that all the required libraries and dependencies are installed correctly on the Raspberry Pis and the control computer.

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the project repository.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [OpenCV](https://opencv.org/) - Computer vision library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Paramiko](https://www.paramiko.org/) - SSH library for Python

## Contact

For any questions or inquiries, please contact the project maintainer at [jessedo@live.com](mailto:jessedo@live.com).
