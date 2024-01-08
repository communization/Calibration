import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk


# Function to display depth at cursor position in Tkinter
def display_depth(event):
    x, y = event.x, event.y
    depth = depth_frame.get_distance(x, y)
    depth_label.config(text=f"Depth: {depth:.3f} meters")


# Start RealSense pipeline    ....
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Tkinter window setup
root = tk.Tk()
root.title("RealSense Camera")
label = tk.Label(root)
label.pack()

# Label to display depth information
depth_label = tk.Label(root, text="Depth: N/A")
depth_label.pack()


# Function to update image in Tkinter window
def update_image():
    global depth_frame
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        root.after(1, update_image)
        return

    # Convert images to numpy arrays and apply colormap
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    depth_colormap = cv2.applyColorMap(
        cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET
    )
    images = np.hstack((color_image, depth_colormap))

    # Convert to PIL Image and display in Tkinter window
    color_image_pil = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
    color_image_tk = ImageTk.PhotoImage(image=color_image_pil)
    label.config(image=color_image_tk)
    label.image = color_image_tk

    root.after(1, update_image)


# Bind the mouse motion event to the label
label.bind("<Motion>", display_depth)

# Start updating the image
root.after(0, update_image)

root.mainloop()

# Stop RealSense pipeline
pipeline.stop()
