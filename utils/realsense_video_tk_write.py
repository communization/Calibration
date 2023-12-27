import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
import os
from PIL import Image, ImageTk


# Function to capture and save image
def capture_image():
    global color_image
    # create folder
    if not os.path.isdir("img"):
        os.mkdir("img")

    # search img name
    for i in range(1, 10000):
        img_name = "img/captured_image_" + str(i) + ".jpg"
        if not os.path.isfile(img_name):
            break

    if color_image is not None:
        cv2.imwrite(img_name, color_image)
        print(f"Image saved as '{img_name}'")


# Function to start video stream
def start_video_stream():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    pipeline.start(config)

    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if not color_frame:
                continue

            global color_image
            color_image = np.asanyarray(color_frame.get_data())

            # Convert to PIL Image and display in Tkinter window
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
