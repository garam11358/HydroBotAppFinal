import cv2
import numpy as np
from matplotlib import pyplot as plt


def o1_Perspective_Transform(title, newPicPath):
    ## 이미지 불러들이기 ##
    img_ori = cv2.imread(title, cv2.IMREAD_GRAYSCALE)
    cv2.namedWindow('Original_Image', cv2.WINDOW_NORMAL)
    cv2.imshow('Original_Image', img_ori)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 이미지 기준 포인트 확인 #
    cv2.circle(img_ori, (60, 465), 5, (255,0,0),-1) #좌상
    cv2.circle(img_ori, (2858,443), 5, (0,255,0),-1) #우상
    cv2.circle(img_ori, (2863,3244), 5, (0,0,225),-1) #우하
    cv2.circle(img_ori, (70,3255), 5, (0,0,0),-1) #좌하

#plt.subplot(121),plt.imshow(img_ori),plt.title('Original_Image')
#plt.show()

## 이미지 좌표 및 변환 좌표 설정, PerspectiveTransform 적용 ##
    pts1 = np.float32([[60, 465],[2858,443],[2863,3244],[70,3255]])
    pts2 = np.float32([[0,0],[1001,0],[1001,1001],[0,1001]])

    M = cv2.getPerspectiveTransform(pts1, pts2)
    img_trans = cv2.warpPerspective(img_ori, M, (1001,1001))

    plt.subplot(121),plt.imshow(img_ori),plt.title('Original_Image')
    plt.subplot(122),plt.imshow(img_trans),plt.title('Transform_Image')
    plt.show()

## 결과 저장 ##
    cv2.imshow('img_trans', img_trans)
    cv2.waitKey(0)
    cv2.imwrite(newPicPath,img_trans)
