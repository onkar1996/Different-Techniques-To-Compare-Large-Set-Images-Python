import imageio
import urllib.request
import cv2
import os
import numpy as np
from urllib.parse import urlparse

def fetchImgGif(url):
    fname = os.path.basename(urlparse(url).path)
    ## Read the gif from the web, save to the disk
    imdata = urllib.request.urlopen(url).read()
    imbytes = bytearray(imdata)
    open(fname,"wb+").write(imdata)
    ## Read the gif from disk to `RGB`s using `imageio.miread` 
    gif = imageio.mimread(fname)
    nums = len(gif)
    #print("Total {} frames in the gif!".format(nums))
    # convert form RGB to BGR 
    imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    return imgs[0]

def fetchImgJpg(url):
    req = urllib.request.urlopen(url)
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    return cv2.imdecode(arr,-1)

def fetchImgFromDiskGif(path):
    gif = imageio.mimread(path)
    imgs = [cv2.cvtColor(img, cv2.COLOR_RGB2BGR) for img in gif]
    return imgs[0]

def fetchImgFromDiskJpg(path):
    return cv2.imread(path)

# 1) Check if 2 images are equal shape
def areImagesEqual(original,imgToCompare):
    if original.shape == imgToCompare.shape:
        print("The images have same size and channels")
        difference = cv2.subtract(original,imgToCompare)
        #cv2.imshow("difference", difference)
        b,g,r = cv2.split(difference)
        if cv2.countNonZero(b)==0 and cv2.countNonZero(b)==0 and cv2.countNonZero(b)==0:
                return "The images are completely equal"
        else :
            return "The images are not equal"

# 2) Check for similarities between 2 images
def checkSimilarities(original,imgToCompare):
    sift = cv2.xfeatures2d.SIFT_create()
    kp_1, desc_1 = sift.detectAndCompute(original,None)
    kp_2, desc_2 = sift.detectAndCompute(imgToCompare,None)
    
    index_params = dict(algorithm=0,trees=5)
    search_params = dict()
    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(desc_1,desc_2,k=2)
    goodPoints = []

    for m,n in matches:
        if m.distance < 0.6*n.distance:
            goodPoints.append(m)
            
    num_keypoints = 0
    if len(kp_1) <= len(kp_2):
        num_keypoints = len(kp_1)
    else:
        num_keypoints = len(kp_2)
    result = cv2.drawMatches(original,kp_1,imgToCompare,kp_2,goodPoints,None)
    cv2.imshow("result",result)
    print("Good points : ", len(goodPoints))
    print("Similarities match % : " + str(int(len(goodPoints)/num_keypoints*100))  + "%")


#If you want to fetch Image from Internet Source
#Pass your values below
URLGIF = ""
URLJPG = ""
original = fetchImgGif(URLGIF)
imgToCompare = fetchImgJpg(URLJPG)
print(areImagesEqual(original,imgToCompare))

checkSimilarities(original,imgToCompare)

cv2.imshow("original", original)
cv2.imshow("imgToCompare", imgToCompare)

cv2.waitKey(0)
cv2.destroyAllWindows()
