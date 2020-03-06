#!/usr/bin/env python3
"""
Sets the modified time of all the JPG images in a folder (and subfolders), using
the information stored in Exif headers. It also (optionally) renames the name
of each file, prepending the image date to the current name
(e.g. 2343.jpg -> 20151231_2343.jpg)

Usage:
# sets date for JPGs in the current folder and subfolders
jpgSetDate.py

# sets date for JPGs in /home/user/images and subfolders
jpgSetDate.py /home/user/images

# sets the date and renames each JPG, prepending the date to the current name
jpgSetDate.py --rename /home/user/images
"""

import argparse
import sys
import os
import os.path
import ntpath
import exifread
from time import localtime, strftime, strptime, mktime
import shutil


def getMinimumCreationTime(exif_data):
    creationTime = None
    dateTime = exif_data.get('DateTime')
    dateTimeOriginal = exif_data.get('EXIF DateTimeOriginal')
    dateTimeDigitized = exif_data.get('EXIF DateTimeDigitized')

    # 3 differnt time fields that can be set independently result in 9 if-cases
    if (dateTime is None):
        if (dateTimeOriginal is None):
            # case 1/9: dateTime, dateTimeOriginal, and dateTimeDigitized = None
            # case 2/9: dateTime and dateTimeOriginal = None, then use dateTimeDigitized
            creationTime = dateTimeDigitized 
        else:
            # case 3/9: dateTime and dateTimeDigitized = None, then use dateTimeOriginal
            # case 4/9: dateTime = None, prefere dateTimeOriginal over dateTimeDigitized
            creationTime = dateTimeOriginal
    else:
        # case 5-9: when creationTime is set, prefere it over the others
        creationTime = dateTime

    return creationTime

def getImageDate(imagePath):
    image = open(imagePath, 'rb')
    creationTime = None
    try: 
        exifTags = exifread.process_file(image, details=False)
        creationTime = getMinimumCreationTime(exifTags)
    except:
        print("invalid exif tags for " + fileName)

    # distinct different time types
    if creationTime is None:
        creationTime = localtime(os.path.getctime(imagePath))
    else:
        try:
            creationTime = strptime(str(creationTime), "%Y:%m:%d %H:%M:%S")
        except:
            creationTime = localtime(os.path.getctime(imagePath))

    image.close()
    return mktime(creationTime)

def processImage(root, image, rename=False):
    imageDate = getImageDate(image)
    creationDate = strftime("%Y%m%d", localtime(imageDate))
    fileName = os.path.basename(image)
    newName = os.path.join(root, creationDate + "_" + fileName)
    os.utime(image, (imageDate, imageDate))
    if rename:
        shutil.move(image, newName)

def processImages(imageDirectory, rename=False):
    images = []
    for root, dirs, files in os.walk(imageDirectory):
        for img in files:
            processImage(root, os.path.join(root, img), rename)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("imageDir", nargs='?', default=os.getcwd(),
                    help="directory to process")
    parser.add_argument("-n", "--rename", action="store_true",
                    help="rename each image prepending the picture date")
    args = parser.parse_args()
    processImages(args.imageDir, args.rename)

if __name__ == '__main__':
    main()

