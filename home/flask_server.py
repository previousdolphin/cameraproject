from flask import Flask, Response, render_template
import cv2
import threading
from video_combining import VideoCombining
from diagnostics import DiagnosticsLogger

app = Flask(__name__)
combining = VideoCombining("192.168.0.2", 8000)  # IP address and port number of Raspberry Pi 1
diagnostics_logger = DiagnosticsLogger("diagnostic.log")

@app.route('/')
def index():
    return render_template('index.html')

def gen_frames():
    while True:
        combined_frame = combining.get_combined_frame()
        if combined_frame is not None:
            ret, buffer = cv2.imencode('.jpg', combined_frame)
            frame = buffer.tobytes()
            diagnostics_logger.log_frame_processing_time()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/diagnostics')
def diagnostics():
    logs = diagnostics_logger.get_logs()
    return render_template('diagnostics.html', logs=logs)

def main():
    def receive_thread():
        combining.receive_frames()

    try:
        combining.start_server()
        receive_thread = threading.Thread(target=receive_thread, daemon=True)
        receive_thread.start()
        diagnostics_logger.start_logging()
        app.run(host='0.0.0.0', port=5000, threaded=True)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
    finally:
        combining.stop_server()
        diagnostics_logger.stop_logging()
        receive_thread.join()

if __name__ == "__main__":
    main()
