import cv2
import threading

class CameraCapture:
    def __init__(self, camera_indices):
        self.camera_indices = camera_indices
        self.cameras = []
        self.frames = {}
        self.capture_threads = []
        self.is_capturing = False

    def start_capture(self):
        for index in self.camera_indices:
            camera = cv2.VideoCapture(index)
            if not camera.isOpened():
                raise RuntimeError(f"Failed to open camera {index}")
            self.cameras.append(camera)

        self.is_capturing = True
        for index in self.camera_indices:
            thread = threading.Thread(target=self.capture_frame, args=(index,))
            thread.start()
            self.capture_threads.append(thread)

    def stop_capture(self):
        self.is_capturing = False
        for thread in self.capture_threads:
            thread.join()

        for camera in self.cameras:
            camera.release()
        self.cameras = []

    def capture_frame(self, camera_index):
        while self.is_capturing:
            ret, frame = self.cameras[camera_index].read()
            if ret:
                self.frames[camera_index] = frame

    def get_frames(self):
        return self.frames

def main():
    camera_indices = [0, 1, 2, 3]  # Adjust the indices based on your camera setup
    capture = CameraCapture(camera_indices)

    try:
        capture.start_capture()
        while True:
            frames = capture.get_frames()
            # Process the captured frames here
            # You can display the frames or perform further operations
            # For example:
            for index, frame in frames.items():
                cv2.imshow(f"Camera {index}", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.stop_capture()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
