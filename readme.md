# Sort files recoverd by Photorec

Photorec does a great job when recovering deleted files. But the result is a huge, unsorted, unnamed amount of files. Especially for external hard drives serving as backup of all the personal data, sortig them is an endless job.

This program helps you sorting your files. First of all, the **files are copied to own folders for each file type**. Second, **jpgs are distinguished by the year** when they have been taken **and by the event**. We thereby define an event as a time span during them photos are taken. It has a delta of 4 days without a photo to another event. If no date from the past can be detected, these jpgs are put into one folder to be sorted manually.


## Usage

```python recovery.py <path to files recovered by Photorec> <destination>```

This copies the recovered file to their file type folder in the destination directory and sets the modification and access time according to EXIF information. The recovered files are not modified. If a file already exists in the destination directory, it is skipped. Hence you can interrupt the process with Ctrl+C and continue afterwards.

The first output of the programm is the number of files to copy. To count them might take some minutes depending on the amount of recovered files. Afterwareds you get some feedback every ~2000 processed files.

All directories contain maximum 500 files. If one contains more, numbered subdirectories are created. If you want another file-limit, e.g. 1000, just put that number as third parameter to the execution of the programm:

```python recovery.py <path to files recovered by Photorec> <destination> 1000```


## Adjust event distance

For the case you want to reduce or increase the timespan between events, simply adjust the variable ```minEventDelta``` in ```jpgSorter.py```. This variable contains the delta between events in seconds.

## jpgSetDate tool

This tools is useful for folders that were sorted using the original version of recovery script, which did not automaticall set the date to the JPGs.

This tool sets the modified time of all the JPG images in a folder (and subfolders), using the information stored in Exif headers. It also (optionally) renames the name of each file, prepending the image date to the current name (e.g. 2343.jpg -> 20151231_2343.jpg)

```
# sets date for JPGs in the current folder and subfolders
python tools/jpgSetDate.py
# sets date for JPGs in /home/user/images and subfolders
python tools/jpgSetDate.py /home/user/images
# sets the date and renames each JPG, prepending the date to the current name
python tools/jpgSetDate.py --rename /home/user/images
```

## jpgSorter tool

jpgSorter can be used now as a standalone tool, which is useful in some particular situations.

Examples:

```
# sorts JPGs in the current folder and subfolders
jpgSorter.py
# sorts JPGs in /home/user/images and subfolders
jpgSorter.py /home/user/images
# sorts JPGs in /home/user/images and subfolders, creating a separate folder per each different day
jpgSorter.py --day /home/user/images
```

