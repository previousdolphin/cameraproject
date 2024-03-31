import cv2
import numpy as np
import open3d as o3d
import threading
import queue

# Global variables
images_queue = queue.Queue()
depth_maps_queue = queue.Queue()
camera_intrinsics_queue = queue.Queue()

def capture_images(camera_ports):
    # Open the cameras
    cameras = [cv2.VideoCapture(port) for port in camera_ports]

    while True:
        # Read frames from the cameras
        frames = [camera.read()[1] for camera in cameras]

        # Add the captured frames to the images queue
        images_queue.put(frames)

def compute_depth_maps(baseline, focal_length):
    while True:
        # Get the latest frames from the images queue
        frames = images_queue.get()

        # Measure depth for each camera pair
        depth_maps = []
        for i in range(0, len(frames), 2):
            left_frame = frames[i]
            right_frame = frames[i+1]
            depth_map = measure_depth(left_frame, right_frame, baseline, focal_length)
            depth_maps.append(depth_map)

        # Add the computed depth maps to the depth maps queue
        depth_maps_queue.put(depth_maps)

def create_3d_model():
    while True:
        # Get the latest depth maps and camera intrinsics from the queues
        depth_maps = depth_maps_queue.get()
        camera_intrinsics = camera_intrinsics_queue.get()

        # Create a point cloud from depth maps and camera intrinsics
        point_cloud = o3d.geometry.PointCloud()
        for depth_map, intrinsic in zip(depth_maps, camera_intrinsics):
            depth_image = o3d.geometry.Image(depth_map)
            intrinsic_matrix = o3d.camera.PinholeCameraIntrinsic()
            intrinsic_matrix.intrinsic_matrix = intrinsic
            pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_image, intrinsic_matrix)
            point_cloud += pcd

        # Estimate normals for the point cloud
        point_cloud.estimate_normals()

        # Create a mesh from the point cloud using Poisson Surface Reconstruction
        mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(point_cloud, depth=8, width=0, scale=1.1, linear_fit=False)[0]

        # Assign texture coordinates to the mesh vertices
        mesh.textures = []
        for image in images_queue.get():
            mesh.textures.append(o3d.geometry.Image(image))

        # Create a texture map for the mesh
        mesh.compute_vertex_normals()
        mesh.compute_triangle_normals()
        mesh.compute_triangle_texture_coordinates()

        # Save the textured 3D mesh to a file
        o3d.io.write_triangle_mesh("output_3d_model.obj", mesh)

def measure_depth(left_image, right_image, baseline, focal_length):
    # Perform depth measurement using stereo images
    # (use the code from the previous examples)
    # ...

    return depth_map

# Example usage
camera_ports = [0, 1, 2, 3, 4, 5, 6, 7]  # Update with the correct camera ports
baseline = 10.0  # Distance between the cameras in centimeters
focal_length = 500.0  # Focal length of the cameras in pixels
camera_intrinsics = [...]  # List of camera intrinsic matrices

# Start the image capture thread
capture_thread = threading.Thread(target=capture_images, args=(camera_ports,))
capture_thread.start()

# Start the depth map computation thread
depth_thread = threading.Thread(target=compute_depth_maps, args=(baseline, focal_length))
depth_thread.start()

# Start the 3D model creation thread
model_thread = threading.Thread(target=create_3d_model)
model_thread.start()

# Add camera intrinsic matrices to the queue
for intrinsic in camera_intrinsics:
    camera_intrinsics_queue.put(intrinsic)

# Wait for the threads to complete (optional)
capture_thread.join()
depth_thread.join()
model_thread.join()
