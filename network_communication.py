import socket
import struct
import pickle
import threading

class NetworkCommunication:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.Lock()

    def connect(self):
        self.sock.connect((self.server_ip, self.server_port))

    def send_frame(self, frame):
        with self.lock:
            data = pickle.dumps(frame)
            size = len(data)
            self.sock.sendall(struct.pack("L", size) + data)

    def close(self):
        self.sock.close()

def main():
    server_ip = "192.168.0.2"  # IP address of Raspberry Pi 2
    server_port = 8000  # Port number for communication

    camera_indices = [0, 1, 2, 3]  # Adjust the indices based on your camera setup
    capture = CameraCapture(camera_indices)
    stitching = VideoStitching(camera_indices)
    communication = NetworkCommunication(server_ip, server_port)

    def stitch_and_send_thread():
        while True:
            frames = capture.get_frames()
            frame_list = [frames[i] for i in camera_indices]
            stitching.stitch_frames(frame_list)
            stitched_frame = stitching.get_stitched_frame()
            if stitched_frame is not None:
                communication.send_frame(stitched_frame)

    try:
        communication.connect()
        capture.start_capture()
        threading.Thread(target=stitch_and_send_thread, daemon=True).start()

        while True:
            # You can perform other tasks or monitoring here
            pass

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
    finally:
        capture.stop_capture()
        communication.close()

if __name__ == "__main__":
    main()
