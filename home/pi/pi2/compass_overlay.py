import cv2
import numpy as np
import math

class CompassOverlay:
    def __init__(self, width, height, compass_size=100, compass_position=(50, 50)):
        self.width = width
        self.height = height
        self.compass_size = compass_size
        self.compass_position = compass_position
        self.compass_image = self.create_compass_image()

    def create_compass_image(self):
        compass_image = np.zeros((self.height, self.width, 4), dtype=np.uint8)
        center_x, center_y = self.compass_position
        radius = self.compass_size // 2

        cv2.circle(compass_image, (center_x, center_y), radius, (255, 255, 255, 255), -1)
        cv2.circle(compass_image, (center_x, center_y), radius, (0, 0, 0, 255), 2)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        font_thickness = 2

        directions = ['N', 'E', 'S', 'W']
        for i, direction in enumerate(directions):
            angle = math.radians(i * 90)
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y - radius * math.sin(angle))
            cv2.putText(compass_image, direction, (x-10, y+10), font, font_scale, (0, 0, 0, 255), font_thickness)

        return compass_image

    def overlay_compass(self, frame):
        alpha = self.compass_image[:, :, 3] / 255.0
        frame_with_compass = frame.copy()
        for c in range(3):
            frame_with_compass[:, :, c] = (1 - alpha) * frame[:, :, c] + alpha * self.compass_image[:, :, c]
        return frame_with_compass

def main():
    combining = VideoCombining("192.168.0.2", 8000)  # IP address and port number of Raspberry Pi 2
    compass_overlay = CompassOverlay(width=640, height=480)  # Adjust the width and height based on your video resolution

    def receive_and_overlay_thread():
        while True:
            combined_frame = combining.get_combined_frame()
            if combined_frame is not None:
                frame_with_compass = compass_overlay.overlay_compass(combined_frame)
                combining.set_combined_frame(frame_with_compass)

    try:
        combining.start_server()
        threading.Thread(target=combining.receive_frames, daemon=True).start()
        threading.Thread(target=receive_and_overlay_thread, daemon=True).start()

        while True:
            # You can perform other tasks or monitoring here
            pass

    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down.")
    finally:
        combining.sock.close()

if __name__ == "__main__":
    main()
