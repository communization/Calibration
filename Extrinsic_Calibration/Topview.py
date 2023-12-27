import cv2
import numpy as np



# 원본 이미지에서 4개의 점을 선택합니다. (x,y)
src_pts = np.array([[0, 0], [0, 360], [640, 360], [640, 0]], dtype=np.float32) 

# 위에서 본 관점의 4개의 대상 점을 선택합니다. (x,y)
dst_pts = np.array([[0, 0], [85, 375], [275, 375], [360, 0]], dtype=np.float32)
# 변환 행렬을 얻습니다.
M = cv2.getPerspectiveTransform(src_pts, dst_pts)

# 원본 이미지를 불러옵니다.
img = cv2.imread('0.jpg')
print(img.shape)

# 투영 변환을 적용합니다.
dst = cv2.warpPerspective(img, M, (360, 600))

# 결과 이미지를 저장합니다.
cv2.imshow('top_view_image.jpg', dst)
cv2.imshow('orinal_image.jpg', img) 

cv2.imshow('top_view_image1.jpg', img[0:200, 0:200])

cv2.waitKey(0)
cv2.destroyAllWindows()