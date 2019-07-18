import cv2
import numpy as np

# 样例图片
img = cv2.imread("screenshot.png")


# 颜色阈值 Upper
upperb = None
# 颜色阈值 Lower
lowerb = None


# 更新MASK图像，并且刷新windows
def updateMask():
    global img
    global lowerb
    global upperb


# 计算MASK
mask = cv2.inRange(img, lowerb, upperb)

cv2.imshow('mask', mask)

# 更新阈值
def updateThreshold(x):

    global lowerb
    global upperb

    minR = cv2.getTrackbarPos('minR', 'image')
    maxR = cv2.getTrackbarPos('maxR', 'image')
    minG = cv2.getTrackbarPos('minG', 'image')
    maxG = cv2.getTrackbarPos('maxG', 'image')
    minB = cv2.getTrackbarPos('minB', 'image')
    maxB = cv2.getTrackbarPos('maxB', 'image')

    lowerb = np.int32([minB, minG, minR])
    upperb = np.int32([maxB, maxG, maxR])

    print('更新阈值')
    print(lowerb)
    print(upperb)
    updateMask()

    cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)
    # cv2.namedWindow('image')
    cv2.imshow('image', img)

    # cv2.namedWindow('mask')
    cv2.namedWindow('mask', flags=cv2.WINDOW_NORMAL | cv2.WINDOW_FREERATIO)

    # 红色阈值 Bar
    ## 红色阈值下界
    cv2.createTrackbar('minR', 'image', 0, 255, updateThreshold)
    ## 红色阈值上界
    cv2.createTrackbar('maxR', 'image', 0, 255, updateThreshold)
    ## 设定红色阈值上界滑条的值为255
    cv2.setTrackbarPos('maxR', 'image', 255)
    # 绿色阈值 Bar
    cv2.createTrackbar('minG', 'image', 0, 255, updateThreshold)
    cv2.createTrackbar('maxG', 'image', 0, 255, updateThreshold)
    cv2.setTrackbarPos('maxG', 'image', 255)
    # 蓝色阈值 Bar
    cv2.createTrackbar('minB', 'image', 0, 255, updateThreshold)
    cv2.createTrackbar('maxB', 'image', 0, 255, updateThreshold)
    cv2.setTrackbarPos('maxB', 'image', 255)

    # 首次初始化窗口的色块
    # 后面的更新 都是由getTrackbarPos产生变化而触发
    updateThreshold(None)

    print("调试棋子的颜色阈值, 键盘摁e退出程序")
    while cv2.waitKey(0) != ord('e'):
        continue

    cv2.destroyAllWindows()