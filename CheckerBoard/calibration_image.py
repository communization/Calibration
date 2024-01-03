# https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html
import pyrealsense2 as rs
import numpy as np
import cv2

board_shape = (7, 10)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

objp = np.zeros((board_shape[0] * board_shape[1], 3), np.float32)
objp[:, :2] = np.mgrid[0 : board_shape[0], 0 : board_shape[1]].T.reshape(-1, 2)

for i in range(0, 6):
    color_image = cv2.imread(f"img/captured_image_{i}.jpg")
    gray = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    retval, corners = cv2.findChessboardCorners(
        gray, (board_shape[0], board_shape[1]), None
    )  # (8-1, 11-1) 정확하게 표기.

    if retval:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        cv2.drawChessboardCorners(
            color_image, (board_shape[0], board_shape[1]), corners, retval
        )

        # Show images
        cv2.imshow("RealSense", color_image)
        cv2.waitKey(100)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

img = cv2.imread("img/captured_image_5.jpg")
h, w = img.shape[:2]
newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
    mtx, dist, (w, h), 1, (w, h)
)  # alpha=1 이면, 모든 픽셀을 포함하는 영상을 만든다.
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
x, y, w, h = roi
dst = dst[y : y + h, x : x + w]
cv2.imwrite("calibresult.png", dst)
