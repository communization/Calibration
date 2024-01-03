import pyrealsense2 as rs
import numpy as np
import cv2

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start the pipeline
pipeline.start(config)

try:
    while True:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        color_image = np.asanyarray(color_frame.get_data())
        print("color_image_max", np.max(color_image))
        retval, corners = cv2.findChessboardCorners(
            color_image, (3, 3), 50
        )  # flags의미 :
        # corner에 대한 좌표 표시
        cv2.drawChessboardCorners(color_image, (5, 5), corners, retval)
        print("corners", corners)
        print("retval", retval)
        # Show images
        cv2.namedWindow("RealSense", cv2.WINDOW_AUTOSIZE)
        cv2.imshow("RealSense", color_image)
        cv2.waitKey(1)

finally:
    # Stop streaming
    pipeline.stop()
