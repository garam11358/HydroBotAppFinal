import opencv
import numpy as np
#import pandas as pd
from matplotlib import pyplot as plt

def o3_Shape_factor_extraction(title, newPicPath):
## 이미지 불러들이기 ##
    img_final = opencv.imread(title)
    img_final_G = opencv.cvtColor(img_final, opencv.COLOR_BGR2GRAY)
    ret, img_binary = opencv.threshold(img_final_G, 127, 255, 0)
#opencv.namedWindow('img_final_G', opencv.WINDOW_NORMAL)
#opencv.imshow('img_final_G', img_binary)
#opencv.waitKey(0)


## 윤곽선 추출 ##
    contours, hierarchy = opencv.findContours(img_binary, opencv.RETR_EXTERNAL, opencv.CHAIN_APPROX_NONE) # 윤곽선 추출
    nlabels, labels, stats, centroids = opencv.connectedComponentsWithStats(img_binary) # 레이블링 추출

    pxsize = 0.02 #1픽셀당 0.02 mm
    i = 0
    area_list = []
    eqd_list = []
    peri_list = []
    longest_list = []
    shortest_list = []
    Ar_list = []


    for cnt in range(len(contours)):
        rect = opencv.minAreaRect(contours[cnt])
        (x, y), (width, height), angle = rect
        min_size = 6
        if width < min_size and height < min_size: # 장단축 4mm이상 0.01mm이하 데이터 에러처리
            continue
        
        i = i+1 #추출개수
        opencv.drawContours(img_final, [contours[cnt]], -1, (255,0,0), 1)
        opencv.putText(img_final, str(i), (int(x), int(y)), 6, 3.0, (255, 0, 0),3)
        area = opencv.contourArea(contours[cnt])*pxsize*pxsize   # 면적
        equi_diameter = np.sqrt(4*area/np.pi)  # 공칭직경
        perimeter = opencv.arcLength(contours[cnt],True)*pxsize   # 둘레길이
        longest = max(width, height)*pxsize
        shortest = min(width, height)*pxsize
        aspect_ratio = min(width, height) / max(width, height) # 종횡비       
        
        area_list.append(area) 
        eqd_list.append(equi_diameter)
        peri_list.append(perimeter)
        longest_list.append(longest)
        shortest_list.append(shortest)
        Ar_list.append(aspect_ratio)

# 입자추출 총 개수/평균면적/평균공칭직경/평균둘레길이/평균종횡비
    print(i, sum(area_list)/len(area_list), sum(eqd_list)/len(eqd_list), sum(peri_list)/len(peri_list), sum(Ar_list)/len(Ar_list))        

# 윤곽선 및 라벨링 결과
#plt.imshow(img_final), plt.title('Contour & Labeling')
#plt.show()
#opencv.waitKey(0)

# Shape parameter histogram 
#bins_num = 10 
    f, ax = plt.subplots(nrows=2, ncols=3, figsize=(15,12))
    f.canvas.set_window_title('Image_result')
#ax[0, 0].set_title("Area", fontsize=16)  
    ax[0, 0].set_xlabel("Area [$mm^2$]", fontsize=16)
    ax[0, 0].set_ylabel("Count", fontsize=16) 
    ax[0, 0].hist(area_list, color='b', edgecolor='black')

    ax[0, 1].set_xlabel("Equivalent diameter [$mm$]", fontsize=16)
    ax[0, 1].set_ylabel("Count", fontsize=16) 
    ax[0, 1].hist(eqd_list, color='b', edgecolor='black')

    ax[0, 2].set_xlabel("Perimeter [$mm$]", fontsize=16)
    ax[0, 2].set_ylabel("Count", fontsize=16) 
    ax[0, 2].hist(peri_list, color='b', edgecolor='black')

    ax[1, 0].set_xlabel("longest axis [$mm$]", fontsize=16)
    ax[1, 0].set_ylabel("Count", fontsize=16) 
    ax[1, 0].hist(longest_list, color='b', edgecolor='black')

    ax[1, 1].set_xlabel("shortest axis [$mm$]", fontsize=16)
    ax[1, 1].set_ylabel("Count", fontsize=16) 
    ax[1, 1].hist(shortest_list, color='b', edgecolor='black')

    ax[1, 2].set_xlabel("Aspect ratio", fontsize=16)
    ax[1, 2].set_ylabel("Count", fontsize=16) 
    ax[1, 2].hist(Ar_list, color='b', edgecolor='black')

#plt.show()
#opencv.waitKey(0)
#opencv.destroyAllWindows()

## 결과 저장 ##
    dstName = newPicPath
#plt.savefig(dstName)
    plt.savefig(dstName, bbox_inches="tight")
#plt.show()	# 이미지 보여주기
