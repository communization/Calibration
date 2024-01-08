import pyrealsense2 as rs
import numpy as np
import cv2
import tkinter as tk
import os
from PIL import Image, ImageTk
import depthai as dai
import time
import datetime


def start_video():
    global video_record_TF, folder_name
    os.makedirs(folder_name, exist_ok=True)
    video_record_TF = True


def pause_video():
    global video_record_TF
    video_record_TF = False


def save_video():
    global folder_name, video_record_TF
    print(f"Video saved as '{folder_name}'")
    folder_name = folder + time.strftime("%Y%m%d_%H%M%S", time.localtime())
    video_record_TF = False


def record_image():
    global color_image


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
            image_show = cv2.resize(frame, (960, 540))
            cv2.putText(
                image_show,
                f"FPS: {fps:.2f}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            color_image_pil = Image.fromarray(
                cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB)
            )
            color_image_tk = ImageTk.PhotoImage(image=color_image_pil)
            label.config(image=color_image_tk)
            label.image = color_image_tk

            global video_record_TF, folder_name
            if video_record_TF == True:
                for i in range(10000):
                    color_img_name = f"{folder_name}/{i}.jpg"
                    if not os.path.isfile(color_img_name):
                        break

                if color_image is not None:
                    cv2.imwrite(color_img_name, color_image)
                    print(f"Color image saved as '{color_img_name}'")
            root.update()


if __name__ == "__main__":
    # Tkinter window setup
    root = tk.Tk()
    root.title("RealSense Camera")

    label = tk.Label(root)
    label.pack()

    # Button to capture image
    folder = "img/oakd/"
    folder_name = folder + time.strftime("%Y%m%d_%H%M%S", time.localtime())
    # capture_button = tk.Button(root, text="Capture Image", command=record_image)
    # capture_button.pack()

    video_record_TF = False
    start_button = tk.Button(root, text="Start", command=start_video)
    pause_button = tk.Button(root, text="Pause", command=pause_video)
    save_button = tk.Button(root, text="Save", command=save_video)

    start_button.pack()
    pause_button.pack()
    save_button.pack()

    # Start video stream in a separate thread
    import threading

    thread = threading.Thread(target=start_video_stream)
    thread.daemon = True
    thread.start()

    root.mainloop()


# import numpy as np
# import matplotlib.pyplot as plt
# import cv2

# import tkinter as tk
# from tkinter import ttk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from tkinter.filedialog import askopenfilename
# import datetime
# import os
# import depthai as dai


# class PlotCanvas:
#     def __init__(self, root, figsize=(10, 10)):
#         self.ax = plt.gca()
#         self.fig = plt.figure(figsize=figsize)
#         self.canvas = FigureCanvasTkAgg(self.fig, master=root)
#         self.frame = None
#         self.video_save_TF = False
#         self.save_path = None
#         self.save_folder = None
#         self.count = 0

#     def get_canvas(self):
#         return self.canvas

#     def get_figure(self):
#         return self.fig


# def Start_video(plotcanvas):
#     # ret, img = cap.read()
#     print("start: 공사중")
#     plotcanvas.video_save_TF = True


# def Pause_video(plotcanvas):
#     plotcanvas.video_save_TF = False


# def View_video(plotcanvas, qRgb):
#     realframes = qRgb.get()
#     img_color = realframes.get_color_frame()

#     img_color = np.asanyarray(img_color.get_data())
#     img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)  # cv2.COLOR_BGR2RGB

#     # img_color = cv2.   resize(img_color, (2400, 1800), interpolation=cv2.INTER_CUBIC)
#     # img_color = cv2.GaussianBlur(img_color, (5, 5), 0)
#     # img_color = cv2.Canny(img_color, 50, 150)
#     # img_color = cv2.equalizeHist(img_color)

#     x = 3

#     plotcanvas.frame.set_data(img_color)
#     plotcanvas.canvas.draw()

#     if plotcanvas.video_save_TF == True:
#         if not os.path.exists(plotcanvas.save_path + plotcanvas.save_folder):
#             os.makedirs(plotcanvas.save_path + plotcanvas.save_folder)
#         img_color = cv2.cvtColor(img_color, cv2.COLOR_RGB2BGR)
#         saved = cv2.imwrite(
#             f"{plotcanvas.save_path}{plotcanvas.save_folder}{str(plotcanvas.count)}.jpg",
#             img_color,
#         )
#         if saved == False:
#             print("save error")
#         else:
#             print(
#                 f"{plotcanvas.save_path}{plotcanvas.save_folder}{str(plotcanvas.count)}.jpg"
#             )
#         print(
#             f"{plotcanvas.save_path}{plotcanvas.save_folder}{str(plotcanvas.count)}.jpg"
#         )
#         plotcanvas.count += 1

#     root.after(40, View_video, plotcanvas, pipeline)


# def Save_video(plotcanvas):
#     plotcanvas.save_path = "D:/Dataset/prior/"
#     plotcanvas.save_folder = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "/"
#     plotcanvas.count = 0
#     plotcanvas.video_save_TF = False


# def main(plotcanvas, qRgb):
#     # 버튼 생성 및 클릭 이벤트 바인딩
#     button_frame1 = tk.Frame(
#         root,
#         bg="lightblue",
#         highlightbackground="darkblue",
#         highlightthickness=1,
#         relief="groove",
#     )
#     button_frame1.pack(side="top", pady=5)
#     Make_box_button = ttk.Button(
#         button_frame1,
#         text="Start Video",
#         command=lambda: Start_video(plotcanvas),
#     )
#     Make_box_button.pack(side="left", pady=5, padx=10)
#     Pause_video_button = ttk.Button(
#         button_frame1, text="Pause Video", command=lambda: Pause_video(plotcanvas)
#     )
#     Pause_video_button.pack(side="left", pady=5, padx=10)

#     Save_video_button = ttk.Button(
#         button_frame1, text="Save Video", command=lambda: Save_video(plotcanvas)
#     )
#     Save_video_button.pack(side="left", pady=5, padx=10)

#     View_video(plotcanvas, qRgb)
#     # 그림을 캔버스에 삽입하고 Tkinter 창에 표시
#     plotcanvas.canvas.draw()
#     plotcanvas.canvas.get_tk_widget().pack()

#     root.mainloop()


# if __name__ == "__main__":
#     # Tkinter 창 설정
#     root = tk.Tk()
#     root.configure(background="black")
#     plotcanvas = PlotCanvas(root, figsize=(10, 10))

#     # ax,fig 설정
#     ax = plotcanvas.ax
#     fig = plotcanvas.fig
#     canvas = plotcanvas.canvas

#     # web cam load
#     # Configure depth and color streams
#     pipeline = dai.Pipeline()

#     camRgb = pipeline.createColorCamera()
#     camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
#     camRgb.setInterleaved(False)
#     camRgb.setFps(40)

#     rgbout = pipeline.createXLinkOut()
#     rgbout.setStreamName("RGB")
#     camRgb.video.link(rgbout.input)

#     # Start streaming
#     with dai.Device(pipeline) as device:
#         device.startPipeline()

#         qRgb = device.getOutputQueue(name="RGB", maxSize=4, blocking=False)

#         inRgb = qRgb.get()
#         img_color = inRgb.getCvFrame()

#         # set plotcanvas.frame , ax
#         frame = plt.imshow(img_color)  # , cmap='gray'
#         plotcanvas.frame = frame
#         plotcanvas.ax.set_title("asdf")

#         now = datetime.datetime.now()
#         # save_path='D:/OneDrive - Sogang/문서/카카오톡 받은 파일/Realsense_video/'
#         save_path = "img/oakd/"
#         save_folder = (
#             datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + "/"
#         )  # f'{now.hour}_{now.minute}_{now.second}/'

#         plotcanvas.save_path = save_path
#         plotcanvas.save_folder = save_folder

#         main(plotcanvas, qRgb)

#         pipeline.stop()
#         cv2.destroyAllWindows()
