import mysql.connector
import imagehash
import urllib.request
import os
import time
from operator import itemgetter 
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
            time.sleep(0.5)
            remaining_download_tries = remaining_download_tries - 1
            continue
        else:
            break
    return fname

#Any Sample Image URL from Internet to Fetch
imageUrl = ""
image = fetchImg(imageUrl)
imgHash = imagehash.phash(Image.open(image))
os.remove(image)

hashDict = {}

mydb = mysql.connector.connect(host="localhost",user="root",passwd="root",database="sample")
cursor = mydb.cursor()
cursor.execute("select distinct (hash),image_url from cid where hash!=''")
result_set = list(cursor.fetchall())
for hashData in result_set:
    imageHash = imagehash.hex_to_hash(hashData[0])
    hashDict[str(imageHash)]= (imgHash - imageHash)

newDict = dict(sorted(hashDict.items(), key = itemgetter(1))[:5]) 
for keys,values in newDict.items():
    print(keys)
    print(values)
