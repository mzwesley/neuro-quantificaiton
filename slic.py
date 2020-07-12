from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import cv2

font = {'family': 'DejaVu Sans',
        'weight': 'bold',
        'size': 16}

plt.rc('font', **font)

# load the image and convert it to a floating point data type
img = img_as_float(cv2.imread('2-1_85%.jpg'))
img = img[..., ::-1]
fig = plt.figure()

# numbers of segments and the std
segments = slic(img, n_segments=250, sigma=5)

# show the output of SLIC
ax = fig.add_subplot()
ax.set_title("Superpixels -- 250 segments")
ax.imshow(mark_boundaries(img, segments))
plt.axis("off")

# show the plots
plt.show()
