import numpy as np
import cv2
import glob

# ===== 1단계: 카메라 교정 =====

# 체커보드 패턴 설정
checkerboard_size = (7, 10)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# 세계 좌표계의 점 초기화 (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((1, checkerboard_size[0] * checkerboard_size[1], 3), np.float32)
objp[0, :, :2] = np.mgrid[0 : checkerboard_size[0], 0 : checkerboard_size[1]].T.reshape(
    -1, 2
)

# 각 카메라에 대한 이미지 포인트와 객체 포인트 저장
objpoints = []  # 3d point in real world space
imgpoints1 = []  # 2d points in image plane for first camera
imgpoints2 = []  # 2d points in image plane for second camera

# 카메라별 이미지 파일 경로
images1 = glob.glob("img/left/*.jpg")
images2 = glob.glob("img/right/*.jpg")

for img1_path, img2_path in zip(images1, images2):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # 체커보드 코너 찾기
    ret1, corners1 = cv2.findChessboardCorners(gray1, checkerboard_size, None)
    ret2, corners2 = cv2.findChessboardCorners(gray2, checkerboard_size, None)

    if ret1 and ret2:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
        corners2 = cv2.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)
        imgpoints1.append(corners1)
        imgpoints2.append(corners2)

# 각 카메라의 내부 매개변수 및 왜곡 계수 교정
ret1, K1, dist1, rvecs1, tvecs1 = cv2.calibrateCamera(
    objpoints, imgpoints1, gray1.shape[::-1], None, None
)
ret2, K2, dist2, rvecs2, tvecs2 = cv2.calibrateCamera(
    objpoints, imgpoints2, gray2.shape[::-1], None, None
)

# ===== 2단계: 스테레오 카메라 교정 =====

flags = 0
flags |= cv2.CALIB_FIX_INTRINSIC
criteria_stereo = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)

# 스테레오 카메라 교정 및 정확도 향상
ret, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
    objpoints,
    imgpoints1,
    imgpoints2,
    K1,
    dist1,
    K2,
    dist2,
    gray1.shape[::-1],
    criteria_stereo,
    flags,
)

# ===== 3단계: 특징점 추출 및 매칭 =====

# 여기서는 예시로 SIFT 특징점 추출 및 FLANN 기반 매칭을 사용합니다
sift = cv2.SIFT_create()
bf = cv2.BFMatcher()

img1 = cv2.imread("img/LR_3.jpg")
img2 = cv2.imread("img/LR_4.jpg")

kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

matches = bf.knnMatch(des1, des2, k=2)

# Lowe's ratio test
good = []
for m, n in matches:
    if m.distance < 0.75 * n.distance:
        good.append(m)

points1 = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 2)
points2 = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 2)

# ===== 4단계: 3D 위치 계산 =====

# 카메라 투영 행렬
P1 = K1 @ np.hstack((np.eye(3), np.zeros((3, 1))))
P2 = K2 @ np.hstack((R, T.reshape(3, 1)))

# 3D 포인트 트라이앵귤레이션
points4D_hom = cv2.triangulatePoints(P1, P2, points1.T, points2.T)

# 동차 좌표계에서 일반 좌표계로 변환
points3D = points4D_hom[:3] / points4D_hom[3]

# 3D 포인트 출력
print(points3D.T)
