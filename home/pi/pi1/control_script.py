import paramiko
import time

def send_command(hostname, username, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, username=username)
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    ssh.close()
    return output

def start_recording(duration):
    # Send start command to Raspberry Pi 1
    send_command('192.168.0.1', 'pi', f'./start_recording.sh {duration}')
    print(f"Recording started for {duration} seconds.")

def stop_recording():
    # Send stop command to Raspberry Pi 1
    send_command('192.168.0.1', 'pi', './stop_recording.sh')
    print("Recording stopped.")

def retrieve_model():
    # Retrieve the generated 3D model from Raspberry Pi 2
    send_command('192.168.0.2', 'pi', 'scp /home/pi/project/output/output_3d_model.obj user@networked_computer:/path/to/save/')
    print("3D model retrieved successfully.")

# Main program
duration = int(input("Enter the duration of the recording session (in seconds): "))
start_recording(duration)
time.sleep(duration)
stop_recording()
retrieve_model()

### INTEGRATE BELOW

import paramiko
import time
import logging

# Configure logging
logging.basicConfig(filename='control_script.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def send_command(hostname, username, command):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname, username=username)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode('utf-8')
        ssh.close()
        return output
    except paramiko.AuthenticationException:
        logging.error(f'Authentication failed for {hostname}')
    except paramiko.SSHException as e:
        logging.error(f'SSH connection failed for {hostname}: {str(e)}')
    except Exception as e:
        logging.error(f'Error occurred while sending command to {hostname}: {str(e)}')

# ... (rest of the code remains the same)

# Main program
try:
    duration = int(input("Enter the duration of the recording session (in seconds): "))
    start_recording(duration)
    time.sleep(duration)
    stop_recording()
    retrieve_model()
except KeyboardInterrupt:
    logging.info('Recording session interrupted by the user.')
except Exception as e:
    logging.error(f'Error occurred during the recording session: {str(e)}')
