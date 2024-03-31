from flask import Flask, Response
import cv2
import threading
from video_combining import VideoCombining

app = Flask(__name__)

combining = VideoCombining("192.168.0.2", 8000)  # IP address and port number of Raspberry Pi 2

def gen_frames():
    while True:
        combined_frame = combining.get_combined_frame()
        if combined_frame is not None:
            ret, buffer = cv2.imencode('.jpg', combined_frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    def receive_thread():
        combining.receive_frames()

    try:
        combining.start_server()
        threading.Thread(target=receive_thread, daemon=True).start()
        app.run(host='0.0.0.0', port=5000, threaded=True)

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
    finally:
        combining.sock.close()

if __name__ == "__main__":
    main()
