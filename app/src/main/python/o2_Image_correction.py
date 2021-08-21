import opencv
import numpy as np
from matplotlib import pyplot as plt


def o2_Image_correction(title, threshold, newPicPath):
## 이미지 불러들이기 ##
    img_tr = opencv.imread(title)
#opencv.imshow('Tr_Image', img_tr)
#opencv.waitKey(0)

## 이미지 히스토그램 확인 ##
    plt.hist(img_tr.ravel(), 256, [0,256]); 
    plt.show()
#################################################################
## 이미지 Thresholding 적용 ##
## adaptive threshold 적용으로 개선 가능

    threshold_num = threshold
#ret,thresh1 = opencv.threshold(img_tr,threshold_num,255,opencv.THRESH_BINARY)
    ret,thresh2 = opencv.threshold(img_tr,threshold_num,255,opencv.THRESH_BINARY_INV)
#ret,thresh3 = opencv.threshold(img_tr,threshold_num,255,opencv.THRESH_TRUNC)
#ret,thresh4 = opencv.threshold(img_tr,threshold_num,255,opencv.THRESH_TOZERO)
#ret,thresh5 = opencv.threshold(img_tr,threshold_num,255,opencv.THRESH_TOZERO_INV)

#plt.subplot(231),plt.imshow(img_tr),plt.title('Original')
#plt.subplot(232),plt.imshow(thresh1),plt.title('THRESH_BINARY')
    plt.subplot(233),plt.imshow(thresh2),plt.title('THRESH_BINARY_INV')
#plt.subplot(234),plt.imshow(thresh3),plt.title('THRESH_TRUNC')
#plt.subplot(235),plt.imshow(thresh4),plt.title('THRESH_TOZERO')
#plt.subplot(236),plt.imshow(thresh5),plt.title('THRESH_TOZERO_INV')
#plt.show()

## Thresholding 결과중 THRESH_BINARY_INV 적용
    img_tr_th = thresh2.copy() 
    plt.subplot(121),plt.imshow(img_tr),plt.title('Original')
    plt.subplot(122),plt.imshow(img_tr_th),plt.title('THRESH_BINARY_INV')
    plt.show() 

#################################################################
## 이미지 Erosion, Dilation, opening, closing  적용 ##

    kernel = np.ones((5,5),np.uint8) #객체 사이즈에 따라 변경

#img_tr_th_er = opencv.erode(img_tr_th,kernel,iterations = 1) # erosion
#img_tr_th_di = opencv.dilate(img_tr_th,kernel,iterations = 1) # dilation
#img_tr_th_op = opencv.morphologyEx(img_tr_th, opencv.MORPH_OPEN, kernel) # opening
    img_tr_th_cl = opencv.morphologyEx(img_tr_th, opencv.MORPH_CLOSE, kernel) # closing

#plt.subplot(231),plt.imshow(img_tr_th),plt.title('Original')
#plt.subplot(232),plt.imshow(img_tr_th_er),plt.title('erosion')
#plt.subplot(233),plt.imshow(img_tr_th_di),plt.title('dilation')
#plt.subplot(234),plt.imshow(img_tr_th_op),plt.title('opening')
#plt.subplot(235),plt.imshow(img_tr_th_cl),plt.title('closing')
#plt.show()

## 이미지 closing  적용 
    plt.subplot(121),plt.imshow(img_tr_th),plt.title('THRESH_BINARY_INV')
    plt.subplot(122),plt.imshow(img_tr_th_cl),plt.title('closing')
    plt.show() 

### 이미지 보정 end ##
    img_final = img_tr_th_cl.copy()
    plt.subplot(121),plt.imshow(img_tr),plt.title('img_tr')
    plt.subplot(122),plt.imshow(img_final),plt.title('img_final')
    plt.show()

## 결과 저장 ##
    opencv.imshow('img_final', img_final)
    opencv.waitKey(0)
    opencv.imwrite(newPicPath,img_final)





