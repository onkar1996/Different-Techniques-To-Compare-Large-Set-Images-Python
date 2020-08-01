from django.http import HttpResponse
import mysql.connector
import imagehash
import os
import time
import json
from operator import itemgetter 
from PIL import Image
from PIL import ImageFile
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import FileSystemStorage
ImageFile.LOAD_TRUNCATED_IMAGES = True

# Create your views here
@csrf_exempt
def home(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        image = fs.url(filename)
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
        return HttpResponse(json.dumps(newDict))
