import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
import os
from PIL import Image, ImageTk


# Function to capture and save color and depth images
def capture_image():
    global color_image, depth_image
    # create folders
    if not os.path.isdir("img"):
        os.makedirs("img/color", exist_ok=True)
        os.makedirs("img/depth", exist_ok=True)

    # search img name
    for i in range(10000):
        color_img_name = f"img/color/C_{i}.jpg"
        depth_img_name = f"img/depth/D_{i}.jpg"
        if not (os.path.isfile(color_img_name) or os.path.isfile(depth_img_name)):
            break

    if color_image is not None and depth_image is not None:
        cv2.imwrite(color_img_name, color_image)
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
        )
        cv2.imwrite(depth_img_name, depth_image)
        print(f"Color image saved as '{color_img_name}'")
        print(f"Depth image saved as '{depth_img_name}'")


# Function to start video stream
def start_video_stream():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # z16
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()
            if not color_frame or not depth_frame:
                continue

            global color_image, depth_image
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())
            print(np.max(depth_image))
            # Convert color image to PIL Image and display in Tkinter window
            color_image_pil = Image.fromarray(
                cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            )
            color_image_tk = ImageTk.PhotoImage(image=color_image_pil)
            label.config(image=color_image_tk)
            label.image = color_image_tk

            root.update()

    finally:
        pipeline.stop()


# Tkinter window setup
root = tk.Tk()
root.title("RealSense Camera")

label = tk.Label(root)
label.pack()

# Button to capture image
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack()

# Start video stream in a separate thread
import threading

thread = threading.Thread(target=start_video_stream)
thread.daemon = True
thread.start()

root.mainloop()
