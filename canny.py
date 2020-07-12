import cv2
import sys


def CannyGuassian(lowThreshold):
    detected_edges = cv2.GaussianBlur(gray, (3, 3), 0)
    detected_edges = cv2.Canny(detected_edges, lowThreshold,
                               lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(img, img, mask=detected_edges)
    cv2.imshow('canny guassian', dst)


def CannyMedian(lowThreshold):
    detected_edges = cv2.medianBlur(gray, 3)
    detected_edges = cv2.Canny(detected_edges, lowThreshold,
                               lowThreshold * ratio, apertureSize=kernel_size)
    dst = cv2.bitwise_and(img, img, mask=detected_edges)
    cv2.imshow('canny median', dst)


lowThreshold = 0  # setting the default threshold
max_lowThreshold = 200
ratio = 3
kernel_size = 3

img = cv2.imread('2-1_85%.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow('canny median', cv2.WINDOW_NORMAL)
cv2.namedWindow('canny guassian', cv2.WINDOW_NORMAL)

cv2.createTrackbar('Min threshold', 'canny median', lowThreshold, max_lowThreshold, CannyMedian)
cv2.createTrackbar('Min threshold', 'canny guassian', lowThreshold, max_lowThreshold, CannyGuassian)

CannyMedian(0)  # low bound threshold
CannyGuassian(0)


if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()
elif cv2.waitKey(0) == ord('s'):
    cv2.imwrite('2-1_85%.tif', img)
    cv2.destroyAllWindows()
