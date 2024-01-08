import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
import os
from PIL import Image, ImageTk
import depthai as dai
import time


def capture_image():
    global color_image, folder_name
    # create folders
    if not os.path.isdir("img"):
        os.makedirs("img/color", exist_ok=True)
        os.makedirs("img/depth", exist_ok=True)

    os.makedirs(folder_name, exist_ok=True)
    # search img name
    for i in range(10000):
        color_img_name = f"{folder_name}/{i}.jpg"
        if not os.path.isfile(color_img_name):
            break

    if color_image is not None:
        cv2.imwrite(color_img_name, color_image)
        print(f"Color image saved as '{color_img_name}'")


# Function to start video stream
def start_video_stream():
    pipeline = dai.Pipeline()

    camRgb = pipeline.createColorCamera()
    camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
    camRgb.setInterleaved(False)
    camRgb.setFps(40)

    rgbout = pipeline.createXLinkOut()
    rgbout.setStreamName("RGB")
    camRgb.video.link(rgbout.input)

    with dai.Device(pipeline) as device:
        device.startPipeline()

        qRgb = device.getOutputQueue(name="RGB", maxSize=4, blocking=False)

        frame_count = 0
        start_time = time.time()
        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived
            frame_count += 1

            # Calculate FPS
            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time > 0:
                fps = frame_count / elapsed_time

            global color_image
            # Display FPS on frame
            frame = inRgb.getCvFrame()
            color_image = cv2.resize(frame, (960, 540))
            cv2.putText(
                color_image,
                f"FPS: {fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            color_image_pil = Image.fromarray(
                cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            )
            color_image_tk = ImageTk.PhotoImage(image=color_image_pil)
            label.config(image=color_image_tk)
            label.image = color_image_tk

            root.update()


# Tkinter window setup
root = tk.Tk()
root.title("RealSense Camera")

label = tk.Label(root)
label.pack()

# Button to capture image
folder_name = "img/oakd/" + time.strftime("%Y%m%d_%H%M%S", time.localtime())
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack()

# Start video stream in a separate thread
import threading

thread = threading.Thread(target=start_video_stream)
thread.daemon = True
thread.start()

root.mainloop()
