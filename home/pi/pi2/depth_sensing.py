import cv2
import numpy as np

def cylindrical_projection(frame, fov_degrees):
    height, width, _ = frame.shape
    fov_radians = np.radians(fov_degrees)

    projected_width = int(width * fov_radians / (2 * np.pi))
    projected_height = height

    projected_img = np.zeros((projected_height, projected_width, 3), dtype=np.uint8)

    center_x = width // 2
    center_y = height // 2

    for i in range(projected_width):
        theta = i * (2 * np.pi) / projected_width
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)

        for j in range(projected_height):
            x = int(center_x + (j - center_y) * sin_theta)
            y = int(center_y + (j - center_y) * cos_theta)

            if 0 <= x < width and 0 <= y < height:
                projected_img[j, i] = frame[y, x]

    return projected_img

# Open the 360° video file
video = cv2.VideoCapture('360_video.mp4')

while True:
    ret, frame = video.read()

    if not ret:
        break

    # Apply cylindrical projection
    fov_degrees = 120  # Field of view in degrees (adjust as needed)
    projected_frame = cylindrical_projection(frame, fov_degrees)

    # Display the projected frame
    cv2.imshow('Cylindrical Projection', projected_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
