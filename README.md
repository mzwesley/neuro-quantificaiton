# Readme

# Sweat Gland Quantification - Image Segmentation
@mzwesley

This is a project that I tried during my leisure time. This project aims at implementing the potential of image segmentation of python into the quantification of sweat gland. This report consists the following 5 parts:
1. **Introduction**, where I explain the problems that I faced when quantifying sweat gland nerve innervation(SGII) during this summer.
2. **Methods**, the part that introduces the image segmentation methods I implemented.
3. **Results**, comparing the sweat gland area quantified by original method used in the lab and the image segmentation methods I applied.
4. **Discussion**, forming possible explaination and hypotheses for the results observed in this project.
5. **Prospect**, the potential future direction of this project.

## Table of Contents

[ToC]

# Introduction
In order to assess the serverity of numerous neurotrophies, quantification of neural density index is essential since it has been proven that sweat gland innervation index (SGII), a neural density index, is a biomarker for amyloid neurotrophy.[[1]](https://www.ncbi.nlm.nih.gov/pubmed/30737830) The current quantification involves using photo editing softwares such as Adobe Photoshop and NIH's ImageJ. These softwares, however, involves tedious work for the experimenter. As a lab intern that had been in that situation, I want ot shorten the quantification process. Therefore, while enrolling in the Bio-programming course, I try to implenment the power of python in the process of quantification.


## SGII
Sweat gland innveration index, also known as SGII, is measured by:

$$
SGII=\frac{A_N}{A_S-A_N}
$$

$A_N=\text{pixel area innverated by neurons}\\
A_S=\text{pixel area innverated by sweat gland tissues}$


The intuition behind is to measure the whole area innverated by sweat gland and neurons and then subtract the area that is innverated by neurons. Figure 1 provides an graphical example.

![](https://i.imgur.com/5PHrjof.jpg =400x) Figure 1 (ref: my experiment)

The blue pixels in figure 1 is the nerve fibers that had been stained by anti-PGP 9.5 antibody. The circular red pixels is sweat gland tissues that had been stained by 1% Congo Red. The pink pixels, however, is dermis, which is irrelevant in our qunatification.

## The Hard Problem
The quantification of SGII has namely the 2 following problems:
1. It usually takes a long time.
2. The boundaries of dermis and sweat gland cannot be identified by photo editing softwares.

Theoretically speaking, time consumption is only a problem for the experimenter, but has no effect on the results. However, in practice, the quality of data might be affected since human has limited stamina. The second problem, on the other hand, has direct impact to the data of SGII. If photo editing softwares cannot successfully identify the edges of dermis and sweat gland, the area of sweat gland can be significantly affected. Therefore, the precise detection of sweat gland is vital to the accuracy of SGII.

## Image Segmentation
With Moore's Law still on the mark, the raise of computing power provides a window of opportunity into analyzing complicated images. Hence, there are various attempts to implenment image segmentation, a subtype of computational vision, to biological methodology. Julien Cohen-Adad and his team from MIT had done a successful implenmentation of neural networks into quantification of axon in rodents' spine.[[2]](https://www.nature.com/articles/s41598-018-22181-4) The following is an graphical example of their results:

![](https://i.imgur.com/MGxxRuu.jpg)

Graphically, results from *AxonDeepSeg* and Gold standard look almost identical. This intrepretation is also backed by statistical data, showing as much as 97% accuracy. Therefore, I want to apply image segmentation into the problems I faced as well.

# Methods
Since there are visible edges between the dermis and sweat gland, my initial thoughts is to find the edges in the image. After little reseach, this hypothesis brings me to Canny edge detection.

For Canny edge detection, I imported the following packages:
1. **opencv-python**, image processing
2. **sys**, taking arguments from terminal

For K-means clustering, I imported the following packages:
1. **opencv-python**, image processing
2. **matplotlib**, plotting comparison figures
3. **os**, for import files since I use jupyter notebook in this case
4. **numpy**, basic mathematical calculations

For SLIC, I imported the following packages:
1. **scikit-image**, built in SLIC function
2. **matplotlib**, plotting comparison figures


## Naive Canny
In this project, Canny edge detection has been used more than once. Hence the term naive canny indicates the method where I simply apply Canny edge detection with different blurring filteres. In order to find the optimal threshold for Canny edge detection, I also utilized the trackbar function in the opencv package. 
```python
# Guassian Filter
cv2.GuassianBlur(gray,(3,3),0)

# Median Filter
cv2.medianBlur(gray,3)

# create trackbar
cv2.createTrackbar('Min threshold', 'canny median', lowThreshold, max_lowThreshold, CannyMedian)
```

The following is a screenshot of the Canny edge detection trackbar:

![](https://i.imgur.com/DZEsN6o.jpg)
+ [original picture of *trackbar_canny*](https://i.imgur.com/DZEsN6o.jpg)

The trackbar enables me to slide through the lower threshold, this makes it a little more convenient to find the threshold that preserves most of the edges while leaving little noise.

After severeal try-and-errors, I found that when lower threshold is around 107, the balance between preserving edges and cancelling noises is the best. Figure 2 gives a two-layer picture that consists edges detected at lower threshold 107 as layer 1 and the original sweat gland tissue as the background.

![](https://i.imgur.com/GBHLEkH.png)
+ [Figure 2](https://i.imgur.com/GBHLEkH.png)

The results generated by naive Canny looks promises at first glance, but more detailed inspection reveals that naive Canny has an inevitable flaw: the dilemma between edges and noise. While it is possible to get rid fo the noise with some processing, but it requires complicated processings that are beyond my ability as of right now. Moreover, the edges that has been detected by naive Canny are not continuous. This could lead to incomplete quantification or over-complete quantification.
![](https://i.imgur.com/m5jGTzb.png)
+ Demostration of the problems generated by solely applying Canny edge detection.

## Naive K-means
K-means clustering is a method of vector quantization.[[4]](https://en.wikipedia.org/wiki/K-means_clustering) Applying K-means clustering into image segmentation would segment the image into *k* cluster. A simple example of K-means clustering in image processing is depicted as the following:
![](https://i.imgur.com/RW5KkgT.png)
+ Figure 4 [[5]](https://rpubs.com/yujingma45/155921)

To apply K-means clustering into quantification of sweat gland, I imported the **opencv** package that contains the k-means function. After several testing, I figured that it is optimal in my case to segment the sweat gland image into **3 clusters**. The reason is that when categorized the image into 2 clusters, the dermis and the sweat gland would be categorized into the same cluster.
![](https://i.imgur.com/KUH3RCA.png)

If $K=4$, the nerve would be partially clustered out, which will also affect the process of quantification.
![](https://i.imgur.com/BZghKx8.png)

If $K>4$, the image would be crowded with noise, which is also not the results we aim for.

Therefore, only when $K=3$ yields the results we want. Visually speaking, the 3 clusters are approximately the dermis, nerve fibers and sweat gland, and background. A comparison diagram compares the original image with $K=3$ image.

![](https://i.imgur.com/Om8aUNN.png)
+ Figure 7 [(See Original)](https://i.imgur.com/Om8aUNN.png)

However, even naive K-means yields results that are not perfect as well.
![](https://i.imgur.com/IgbIJL4.png)



## K-means Canny
While naive K-means delivered unwanted results, it indicates a potential pro-process method. Therefore, I hypothesized that with the help of K-means clustering, canny edge detection can better do its job. 
```mermaid
graph LR
    A["Original IMG"] --> B["K-means Clustering"] --> C["Canny Edge Detection"]
```
With this in mind, I tried edge detecting with the image that had been processed by K-means. The following are the results:

![](https://i.imgur.com/wPmg0ml.png)

As we can see, the edges are now continuous. Furthermore, the distinguishment between dermis and sweat gland are better.

![](https://i.imgur.com/qEhDDgH.jpg)

Overlaying the edges and the original image reveals that this is indeed a great way to detect the sweat gland.

## SLIC
Simple linear iterative clustering is a clustering method based on K-means clustering. This is a method that guarntees convergence. To utilize SLCI, I imported the opencv with the built in function, slic.
![](https://i.imgur.com/AdGRsTk.png)
![](https://i.imgur.com/IoBJNwf.png)

The images above are the being processed with SLIC with the only difference in the number of segments. While SLIC does offer satisfactory results, the number of segments tends to vary tissue by tissue. This could be a huge problem when constructing the operational definition of determining how many segments.

# Results
For this project, I have sampled out the top middle sweat gland:
![](https://i.imgur.com/6Hwz0MI.png)

The following is the quantification results of the respective methods:
![](https://i.imgur.com/5itjsNe.png)

I have also created an interactive photo frame to compare the original image with the image being processed with each of the methods:

**(Simply slide the trackbar in the middle to adjust viewing proportion of the two pictures)**

<iframe frameborder="0" class="juxtapose" width="680" height="510" src="https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=2623b054-183a-11ea-b9b8-0edaf8f81e27"></iframe>


<iframe frameborder="0" class="juxtapose" width="680" height="510" src="https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=6aa322d2-183a-11ea-b9b8-0edaf8f81e27"></iframe>


<iframe frameborder="0" class="juxtapose" width="680" height="510" src="https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=d0f10e8a-17f1-11ea-b9b8-0edaf8f81e27"></iframe>


<iframe frameborder="0" class="juxtapose" width=680 height="510" src="https://cdn.knightlab.com/libs/juxtapose/latest/embed/index.html?uid=c486ff08-183a-11ea-b9b8-0edaf8f81e27"></iframe>


![](https://i.imgur.com/Kyoft7g.png)
![](https://i.imgur.com/xSICWNE.png)

For now, K-means Canny provides the least error with SLIC being the runner-up.

# Discussion
I believe that both SLIC and K-means Canny have the potential to achieve some degree of accuracy at detecting the boundaries between sweat gland and dermis. SLIC, on one hand, provides guranteed continuous edges. However, it may requires more effort in the process of quantification since oftentimes it is better to be conservative at the number of segments, which, namely, overestimate the number of segments is better. But this would require may effort to click the over-divide segments in order to quantify. Therefore, as of right now, I believe that we can implenment a mix of K-means Canny and SLIC during the process of quantification.

# Prospect
This project shortens some time in the process of quantification, however, this is definitely not the real solution yet. In the future, I wish I could develop a neural network that can really automate the process of quantification but also retains the high accuracy as the gold standard of right now.

