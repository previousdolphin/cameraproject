import numpy as np
import open3d as o3d

# ...

def create_3d_model():
    while True:
        # Get the latest depth maps from the queue
        depth_maps = depth_maps_queue.get()

        # Read camera intrinsics
        intrinsics_path = '/home/pi/project/camera_intrinsics/camera_intrinsics.txt'
        camera_intrinsics = read_camera_intrinsics(intrinsics_path)

        # Create a point cloud from depth maps and camera intrinsics
        point_cloud = o3d.geometry.PointCloud()
        for depth_map in depth_maps:
            depth_image = o3d.geometry.Image(depth_map)
            intrinsic_matrix = o3d.camera.PinholeCameraIntrinsic(
                width=640,
                height=480,
                fx=camera_intrinsics['fx'],
                fy=camera_intrinsics['fy'],
                cx=camera_intrinsics['cx'],
                cy=camera_intrinsics['cy']
            )
            pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_image, intrinsic_matrix)
            point_cloud += pcd

        # ...
import cv2
import numpy as np
import os
import time
import open3d as o3d
import yaml

# Load configuration parameters
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

depth_map_folder = config['depth_map_folder']
output_folder = config['output_folder']
intrinsic_matrix = np.array(config['intrinsic_matrix'])

def create_point_cloud(depth_map, intrinsic):
    height, width = depth_map.shape
    fx, fy = intrinsic[0, 0], intrinsic[1, 1]
    cx, cy = intrinsic[0, 2], intrinsic[1, 2]

    point_cloud = []
    for v in range(height):
        for u in range(width):
            depth = depth_map[v, u]
            if depth > 0:
                z = depth / 1000.0  # Convert depth from millimeters to meters
                x = (u - cx) * z / fx
                y = (v - cy) * z / fy
                point_cloud.append([x, y, z])

    return np.array(point_cloud)

def create_3d_model():
    depth_maps = []
    timestamps = []

    # Read depth maps from the folder
    for filename in os.listdir(depth_map_folder):
        if filename.endswith('.png'):
            depth_map = cv2.imread(os.path.join(depth_map_folder, filename), cv2.IMREAD_UNCHANGED)
            depth_maps.append(depth_map)
            timestamps.append(int(filename.split('_')[1].split('.')[0]))

    # Sort depth maps based on timestamps
    depth_maps = [depth_map for _, depth_map in sorted(zip(timestamps, depth_maps))]

    # Create point clouds from depth maps
    point_clouds = []
    for depth_map in depth_maps:
        point_cloud = create_point_cloud(depth_map, intrinsic_matrix)
        point_clouds.append(point_cloud)

    # Combine point clouds
    combined_point_cloud = np.concatenate(point_clouds, axis=0)

    # Create Open3D point cloud object
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(combined_point_cloud)

    # Estimate normals
    pcd.estimate_normals()

    # Create mesh from point cloud
    mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd, depth=8, width=0, scale=1.1, linear_fit=False)[0]

    # Save the 3D model
    timestamp = int(time.time())
    output_filename = os.path.join(output_folder, f'3d_model_{timestamp}.ply')
    o3d.io.write_triangle_mesh(output_filename, mesh)

    print('3D model created successfully.')

# Monitor for new depth maps and create 3D models
while True:
    if len(os.listdir(depth_map_folder)) > 0:
        create_3d_model()
    time.sleep(1)
