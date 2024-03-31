import cv2
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GObject

class RtspServer:
    def __init__(self, port):
        self.port = port
        Gst.init(None)
        self.pipeline = self.create_pipeline()
        self.video_sink = self.pipeline.get_by_name('video_sink')

    def create_pipeline(self):
        pipeline = Gst.parse_launch(f'''
            appsrc name=video_src ! videoconvert ! x264enc tune=zerolatency bitrate=3000 speed-preset=superfast ! rtph264pay config-interval=1 ! udpsink host=127.0.0.1 port={self.port}
        ''')
        return pipeline

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.NULL)

    def push_frame(self, frame):
        data = frame.tobytes()
        buf = Gst.Buffer.new_wrapped(data)
        self.video_sink.emit('push-buffer', buf)

def main():
    rtsp_port = 8554  # Port number for RTSP streaming

    combining = VideoCombining("192.168.0.2", 8000)  # IP address and port number of Raspberry Pi 2
    rtsp_server = RtspServer(rtsp_port)

    def receive_and_stream_thread():
        rtsp_server.start()
        while True:
            combined_frame = combining.get_combined_frame()
            if combined_frame is not None:
                rtsp_server.push_frame(combined_frame)

    try:
        combining.start_server()
        threading.Thread(target=combining.receive_frames, daemon=True).start()
        threading.Thread(target=receive_and_stream_thread, daemon=True).start()

        while True:
            # You can perform other tasks or monitoring here
            pass

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
    finally:
        rtsp_server.stop()
        combining.sock.close()

if __name__ == "__main__":
    main()
