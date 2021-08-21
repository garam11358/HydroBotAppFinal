import opencv
import numpy as np
from matplotlib import pyplot as plt


def o1_Perspective_Transform(title, newPicPath):
    ## 이미지 불러들이기 ##
    img_ori = opencv.imread(title, opencv.IMREAD_GRAYSCALE)
    opencv.namedWindow('Original_Image', opencv.WINDOW_NORMAL)
    opencv.imshow('Original_Image', img_ori)
    opencv.waitKey(0)
    opencv.destroyAllWindows()


# 이미지 기준 포인트 확인 #
    opencv.circle(img_ori, (60, 465), 5, (255,0,0),-1) #좌상
    opencv.circle(img_ori, (2858,443), 5, (0,255,0),-1) #우상
    opencv.circle(img_ori, (2863,3244), 5, (0,0,225),-1) #우하
    opencv.circle(img_ori, (70,3255), 5, (0,0,0),-1) #좌하

#plt.subplot(121),plt.imshow(img_ori),plt.title('Original_Image')
#plt.show()

## 이미지 좌표 및 변환 좌표 설정, PerspectiveTransform 적용 ##
    pts1 = np.float32([[60, 465],[2858,443],[2863,3244],[70,3255]])
    pts2 = np.float32([[0,0],[1001,0],[1001,1001],[0,1001]])

    M = opencv.getPerspectiveTransform(pts1, pts2)
    img_trans = opencv.warpPerspective(img_ori, M, (1001,1001))

    plt.subplot(121),plt.imshow(img_ori),plt.title('Original_Image')
    plt.subplot(122),plt.imshow(img_trans),plt.title('Transform_Image')
    plt.show()

## 결과 저장 ##
    opencv.imshow('img_trans', img_trans)
    opencv.waitKey(0)
    opencv.imwrite(newPicPath,img_trans)






