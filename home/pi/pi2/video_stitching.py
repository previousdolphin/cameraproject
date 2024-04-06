import cv2
import numpy as np
import threading

class VideoStitching:
    def __init__(self, camera_indices, stitch_width=800, stitch_height=600):
        self.camera_indices = camera_indices
        self.stitch_width = stitch_width
        self.stitch_height = stitch_height
        self.stitcher = cv2.createStitcher(cv2.Stitcher_PANORAMA)
        self.stitched_frame = None
        self.lock = threading.Lock()

    def stitch_frames(self, frames):
        # Resize frames to a consistent size
        resized_frames = []
        for frame in frames:
            resized_frame = cv2.resize(frame, (self.stitch_width, self.stitch_height))
            resized_frames.append(resized_frame)

        # Stitch the resized frames
        status, stitched_frame = self.stitcher.stitch(resized_frames)

        if status == cv2.Stitcher_OK:
            with self.lock:
                self.stitched_frame = stitched_frame
        else:
            raise RuntimeError("Failed to stitch frames")

    def post_process_frame(self):
        with self.lock:
            if self.stitched_frame is not None:
                # Perform any necessary post-processing on the stitched frame
                # For example, you can apply image enhancements, cropping, or resizing
                processed_frame = cv2.medianBlur(self.stitched_frame, 3)
                return processed_frame
            else:
                return None

    def get_stitched_frame(self):
        with self.lock:
            return self.stitched_frame

def main():
    camera_indices = [0, 1, 2, 3]  # Adjust the indices based on your camera setup
    capture = CameraCapture(camera_indices)
    stitching = VideoStitching(camera_indices)

    def stitch_thread():
        while True:
            frames = capture.get_frames()
            frame_list = [frames[i] for i in camera_indices]
            stitching.stitch_frames(frame_list)

    try:
        capture.start_capture()
        threading.Thread(target=stitch_thread, daemon=True).start()

        while True:
            processed_frame = stitching.post_process_frame()

            if processed_frame is not None:
                cv2.imshow("Stitched Frame", processed_frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        capture.stop_capture()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
