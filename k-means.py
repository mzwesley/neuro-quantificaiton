import matplotlib.pyplot as plt
import numpy as np
import cv2

original_img = cv2.imread('2-1_85%.jpg')
img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
# M*N*3 image into K*3 (K=M*N) matrix in RGB space
vectorized = img.reshape((-1, 3))
# convert to float
vectorized = np.float32(vectorized)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3  # number of clusters
attempts = 15

ret, label, center = cv2.kmeans(vectorized, K, None, criteria, attempts, cv2.KMEANS_PP_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
result_image = res.reshape((img.shape))
figure_size = 15

plt.figure(figsize=(figure_size, figure_size))
plt.subplot(1, 2, 1), plt.imshow(img)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(1, 2, 2), plt.imshow(result_image)
plt.title('Segmented Image when K = %i' % K), plt.xticks([]), plt.yticks([])
plt.show()
