import os.path
import ntpath
import exifread
from time import localtime, strftime, strptime, mktime
import shutil

minEventDelta = 60 * 60 * 24 * 4 # 4 days in seconds
unknownDateFolderName = "Datum unbekannt"


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

def postprocessImage(images, imageDirectory, fileName):
    imagePath = os.path.join(imageDirectory, fileName)
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

    images.append((mktime(creationTime), imagePath))
    image.close()


def createNewFolder(destinationRoot, year, eventNumber):
    yearPath = os.path.join(destinationRoot, year)
    if not os.path.exists(yearPath):
        os.mkdir(yearPath)
    eventPath = os.path.join(yearPath, str(eventNumber))
    if not os.path.exists(eventPath):
        os.mkdir(eventPath)

def createUnknownDateFolder(destinationRoot):
    path = os.path.join(destinationRoot, unknownDateFolderName)
    if not os.path.exists(path):
        os.mkdir(path)


def writeImages(images, destinationRoot):
    sortedImages = sorted(images)
    previousTime = None
    eventNumber = 0
    today = strftime("%d/%m/%Y")

    for imageTuple in sortedImages:
        destination = ""
        destinationFilePath = ""
        t = localtime(imageTuple[0])
        year = strftime("%Y", t)
        creationDate = strftime("%d/%m/%Y", t)
        fileName = ntpath.basename(imageTuple[1])

        if(creationDate == today):
            createUnknownDateFolder(destinationRoot)
            destination = os.path.join(destinationRoot, unknownDateFolderName)
            destinationFilePath = os.path.join(destination, fileName)
            
        else:
            if (previousTime == None) or ((previousTime + minEventDelta) < imageTuple[0]):
                previousTime = imageTuple[0]
                eventNumber = eventNumber + 1
                createNewFolder(destinationRoot, year, eventNumber)
            
            previousTime = imageTuple[0]

            destination = os.path.join(destinationRoot, year, str(eventNumber))
            # it may be possible that an event covers 2 years. 
            # in such a case put all the images to the even in the old year
            if not (os.path.exists(destination)):
                destination = os.path.join(destinationRoot, str(int(year) - 1), str(eventNumber))

            destinationFilePath = os.path.join(destination, fileName)

        if not (os.path.exists(destinationFilePath)):
            os.utime(imageTuple[1], (imageTuple[0], imageTuple[0]))
            shutil.move(imageTuple[1], destination)
        else:
            if (os.path.exists(imageTuple[1])):
                os.remove(imageTuple[1])

def writeImagesPerDay(images, destinationRoot):
    sortedImages = sorted(images)
    today = strftime("%Y%m%d")

    for imageTuple in sortedImages:
        destination = ""
        destinationFilePath = ""
        t = localtime(imageTuple[0])
        year = strftime("%Y", t)
        creationDate = strftime("%Y%m%d", t)
        fileName = ntpath.basename(imageTuple[1])

        if(creationDate == today):
            createUnknownDateFolder(destinationRoot)
            destination = os.path.join(destinationRoot, unknownDateFolderName)
            destinationFilePath = os.path.join(destination, fileName)
            
        else:
            destination = os.path.join(destinationRoot, year, creationDate)
            if not os.path.exists(destination):
                os.makedirs(destination)
            destinationFilePath = os.path.join(destination, fileName)

        if not (os.path.exists(destinationFilePath)):
            os.utime(imageTuple[1], (imageTuple[0], imageTuple[0]))
            shutil.move(imageTuple[1], destination)
        else:
            if (os.path.exists(imageTuple[1])):
                os.remove(imageTuple[1])


def postprocessImages(imageDirectory, oneFolderPerDay=False):
    images = []
    for root, dirs, files in os.walk(imageDirectory):
        for file in files:
            postprocessImage(images, root, file)
    if oneFolderPerDay:
        # create a subfolder per each different day (e.g. 20151230, 20151231, etc)
        writeImagesPerDay(images, imageDirectory)
    else:
        # group images by event, using a time delta
        writeImages(images, imageDirectory)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("imageDir", nargs='?', default=os.getcwd(),
                    help="directory to process")
    parser.add_argument("-e", "--event", action="store_true",
                    help="create a subfolder per each event. Images are assigned to the same event if they fit within the defined time delta. This is the default behaviour")
    parser.add_argument("-d", "--day", action="store_true",
                    help="create a subfolder per each different day (e.g. 20151230, 20151231, etc). Ignored if -e is provided")
    args = parser.parse_args()
    oneFolderPerDay = args.day and not args.event
    postprocessImages(args.imageDir, oneFolderPerDay)

