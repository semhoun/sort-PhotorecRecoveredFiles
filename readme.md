# Sort files recoverd by Photorec

Photorec does a great job when recovering deleted files. But the result is a huge, unsorted, unnamed amount of files. Especially for external hard drives serving as backup of all the personal data, sorting them is an endless job.

This program sPRF helps you sorting your files. First of all, the **files are copied to own folders for each file type**. Second, **jpgs are distinguished by the year, optionally by month as well or by day** when they have been taken **and by the event**. We thereby define an event as a time span during them photos are taken. It has a delta of 4 days without a photo to another event. If no date from the past can be detected, these jpgs are put into one folder to be sorted manually.

## Quick howto

Use this command, to remove thumb, remove duplicate and sort files

1. Get this repo et go into it
2. Remove thumbs `find <recovered folder> -name "t*" -exec rm -f "{}" \;`
3. Remove duplicate with: ``./rmDuplicate <recovered folder>``
4. Sort files ``./recovery.py <recovered folder> <dest> -k -d -r``
5. Rename jpeg ``./jpgSetDate.py --rename <dest jpeg folder>``

## Installation

First install the package [exifread](https://pypi.python3.org/pypi/ExifRead):

```pip3 install exifread```

## Run the sorter

Then run the sorter:

```python3 recovery.py <path to files recovered by Photorec> <destination>```

This copies (*if you don't ask to move with -r*) the recovered file to their file type folder in the destination directory. The recovered files are not modified. If a file already exists in the destination directory, it is skipped. Hence you can interrupt the process with Ctrl+C and continue afterwards.

The first output of the programm is the number of files to copy. To count them might take some minutes depending on the amount of recovered files. Afterwareds you get some feedback on the processed files.

### Parameters

For an overview of all arguments, run with the `-h` option: ```python3 recovery.py -h```.

#### Max numbers of files per folder

All directories contain maximum 500 files. If one contains more, numbered subdirectories are created. If you want another file-limit, e.g. 1000, just put that number as third parameter to the execution of the program:

```python3 recovery.py <path to files recovered by Photorec> <destination> -n1000```

#### Folder for each month

sPRF usually sorts your photos by year:

```
destination
|- 2015
    |- 1.jpg
    |- 2.jpg
    |- ...
|- 2016
    |- ...
```

Sometimes you might want to sort each year by month:

```python3 recovery.py <path to files recovered by Photorec> <destination> -m```

Now you get:

```
destination
|- 2015
    |- 1
      |- 1.jpg
      |- 2.jpg
    |- 2
      |- 3.jpg
      |- 4.jpg
    |- ...
|- 2016
    |- ...
```

#### Keep original filenames

Use the -k parameter to keep the original filenames:

```python3 recovery.py <path to files recovered by Photorec> <destination> -k```


#### Adjust event distance

For the case you want to reduce or increase the timespan between events, simply use the parameter -d. The default is 4:
```python3 recovery.py <path to files recovered by Photorec> <destination> -d10```

## jpgSetDate tool

This tools is useful for folders that were sorted using the original version of recovery script, which did not automaticall set the date to the JPGs.

This tool sets the modified time of all the JPG images in a folder (and subfolders), using the information stored in Exif headers. It also (optionally) renames the name of each file, prepending the image date to the current name (e.g. 2343.jpg -> 20151231_2343.jpg)

```
# sets date for JPGs in the current folder and subfolders
python3 jpgSetDate.py
# sets date for JPGs in /home/user/images and subfolders
python3 jpgSetDate.py /home/user/images
# sets the date and renames each JPG, prepending the date to the current name
python3 jpgSetDate.py --rename /home/user/images
```

## jpgSorter tool

jpgSorter can be used now as a standalone tool, which is useful in some particular situations.

Examples:

```
# sorts JPGs in the current folder and subfolders
python3 jpgSorter.py
# sorts JPGs in /home/user/images and subfolders
python3 jpgSorter.py /home/user/images
# sorts JPGs in /home/user/images and subfolders, creating a separate folder per each different day
python3 jpgSorter.py --day /home/user/images
# sorts JPGs in /home/user/images and subfolders, creating a separate folder per each different month
python3 jpgSorter.py --month /home/user/images
```