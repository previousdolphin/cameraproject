from flask import Flask, Response, render_template
import cv2
import threading
import paramiko
from diagnostics import DiagnosticsLogger

app = Flask(__name__)
diagnostics_logger = DiagnosticsLogger("diagnostic.log")

# SSH connection details for Raspberry Pi 1
pi1_hostname = "192.168.0.2"  # Replace with the IP address of Raspberry Pi 1
pi1_username = "pi"  # Replace with the username for Raspberry Pi 1
pi1_password = "raspberry"  # Replace with the password for Raspberry Pi 1

# SSH connection details for Raspberry Pi 2
pi2_hostname = "192.168.0.3"  # Replace with the IP address of Raspberry Pi 2
pi2_username = "pi"  # Replace with the username for Raspberry Pi 2
pi2_password = "raspberry"  # Replace with the password for Raspberry Pi 2

def ssh_command(hostname, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(command)
    ssh.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_capture')
def start_capture():
    command = "python /path/to/raspberry_pi_1/capture_images.py"
    threading.Thread(target=ssh_command, args=(pi1_hostname, pi1_username, pi1_password, command)).start()
    return "Image capture started on Raspberry Pi 1"

@app.route('/start_3d_modeling')
def start_3d_modeling():
    command = "python /path/to/raspberry_pi_2/create_3d_model.py"
    threading.Thread(target=ssh_command, args=(pi2_hostname, pi2_username, pi2_password, command)).start()
    return "3D modeling started on Raspberry Pi 2"

@app.route('/diagnostics')
def diagnostics():
    logs = diagnostics_logger.get_logs()
    return render_template('diagnostics.html', logs=logs)

def main():
    try:
        diagnostics_logger.start_logging()
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
    finally:
        diagnostics_logger.stop_logging()

if __name__ == "__main__":
    main()
