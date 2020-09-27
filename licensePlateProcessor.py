import os, io
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image
import pandas as pd
import re, findCustomer as find


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'AutoNationChallenge-GoogleVision.json'
file_name = os.path.abspath(r'LicensePlateSamples/7.jpg')


def findCar(img):
    """Finds the bounds of a car object, and crops the picture based on that car"""
    
    buffer = io.BytesIO()
    img.save(buffer,"PNG")
    content = buffer.getvalue()
    image = vision.types.Image(content=content)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    carFound = False
    for obj in localized_object_annotations:
        if obj.name == "Car":
            carFound = True
            p1=obj.bounding_poly.normalized_vertices[0]
            p2=obj.bounding_poly.normalized_vertices[1]
            p3=obj.bounding_poly.normalized_vertices[2]
            p4=obj.bounding_poly.normalized_vertices[3]

    if (carFound) :
        pt1 = [min(p1.x, p2.x, p3.x, p4.x), min(p1.y, p2.y, p3.y, p4.y)]
        pt2 = [max(p1.x, p2.x, p3.x, p4.x), max(p1.y, p2.y, p3.y, p4.y)]
        width, height = img.size
        im2 = img.crop((pt1[0] * width, pt1[1] * height, pt2[0] * width, pt2[1] * height))
        return im2


def findPlate(img):
    """Finds the bounds of a license plate object, and crops the picture based on that license plate"""

    buffer = io.BytesIO()
    img.save(buffer,"PNG")
    content = buffer.getvalue()
    image = vision.types.Image(content=content)
    response = client.object_localization(image=image)
    localized_object_annotations = response.localized_object_annotations
    licensePlateFound = False

    for obj in localized_object_annotations:
        if obj.name == "License plate":
            licensePlateFound = True
            p1=obj.bounding_poly.normalized_vertices[0]
            p2=obj.bounding_poly.normalized_vertices[1]
            p3=obj.bounding_poly.normalized_vertices[2]
            p4=obj.bounding_poly.normalized_vertices[3]

    if (licensePlateFound) :
        pt1 = [min(p1.x, p2.x, p3.x, p4.x), min(p1.y, p2.y, p3.y, p4.y)]
        pt2 = [max(p1.x, p2.x, p3.x, p4.x), max(p1.y, p2.y, p3.y, p4.y)]
        width, height = img.size
        im2 = img.crop((pt1[0] * width, pt1[1] * height, pt2[0] * width, pt2[1] * height))
        buffer = io.BytesIO()
        im2.save(buffer,"PNG")
        return buffer
    else :
        newImg = findCar(img)
        if(newImg != None):
            return findPlate(newImg)


image = Image.open(file_name)
client = vision.ImageAnnotatorClient()

buffer = findPlate(image)

if(buffer == None):
    exit()

content = buffer.getvalue()
newImage = types.Image(content=content)
response = client.text_detection(image=newImage)
texts = response.full_text_annotation

i = 0
blockNum = 0
maxFontBlock = 0

for page in texts.pages:
    for block in page.blocks:
        if maxFontBlock < (block.bounding_box.vertices[2].y - block.bounding_box.vertices[0].y) :
            maxFontBlock = block.bounding_box.vertices[2].y - block.bounding_box.vertices[0].y
            blockNum = i
        i += 1    

str = ''

for paragraph in texts.pages[0].blocks[blockNum].paragraphs:
    for word in paragraph.words:
        for symbol in word.symbols:
            str += symbol.text

str = re.sub(r'\W+', '', str)

print("License Plate Found: " + str)
find.findCustomer(str)