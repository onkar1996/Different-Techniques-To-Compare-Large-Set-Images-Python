import mysql.connector
import imagehash
import imageio
import urllib.request
import cv2
import os
import numpy as np
import time
from urllib.parse import urlparse
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

def fetchImg(url):
    fname = os.path.basename(urlparse(url).path)
    remaining_download_tries = 20
    while remaining_download_tries > 0 :
        try:
            req = urllib.request.urlretrieve(url,fname)
            print("successfully downloaded..!!")
            break
        except:
            print("error downloading on trial no: " + str(21 - remaining_download_tries))
            time.sleep(1)
            remaining_download_tries = remaining_download_tries - 1
            continue
        else:
            break
    return fname

mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="sample")
cursor = mydb.cursor()
cursor.execute("select image_url from cid where hash=''")
result_set = list(cursor.fetchall())
counter=0
for imageUrl in result_set:
    image = fetchImg(imageUrl[0])
    imgHash = imagehash.phash(Image.open(image))
    os.remove(image)
    cursor.execute (""" UPDATE cid SET hash=%s WHERE image_url = %s """,(str(imgHash),str(imageUrl[0])))
    print(counter)
    counter+=1
mydb.commit()
