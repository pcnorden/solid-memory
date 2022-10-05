# solid-memory
This is a side project that I'm making for work where I need to calibrate a lot of dial indicators, which would require a lot of image processing since the dial indicators are the cheap kind that doesn't use any sort of electronics to measure distance.

This is very much a side project that will be worked on-and-off through my spare time and have no clear direction, but hopefully once more features are added, this readme will include more information.

# Screenshot
Well, first of all, this window is created by a testing script that I have for playing around in and this is not yet in the software, but the pink circles in the image are the graduations found on a dial indicator face.

![Screenshot of testing software](./images/Testing_screenshot2022.png)

# How to run
This software is mostly developed in python and opencv under linux enviroments so Mac and Windows platforms I don't care about.

## Prerequesits
1. Have python 3 installed ofcourse, since python 2 is long since EOL.

2. Have a somewhat recent version of opencv-python package installed. For me on Ubuntu it was installed through  
`pip3 install opencv-python`  
on the command line.

# Files

`reading.py` is the current program where things are getting developed and getting things to extract angles and such between lines on the dial face. Lots of comments to be written to document the software there yet to come, but main place where you will see things happening.

`sensing.py` This was version 1 of the program that was made, but due to better comments, it's staying around for right now until I have documented the whole of reading.py and then this file will be basically bulldozered and rebuilt with the main logic of the program and maybe some fanzy Qt UI if I ever can get to grips to understand how that works.

## Image files

|Filename|Description|Current state|
|---|---|---|
|`dial.jpg`|This is a closeup of a Mitutoyo dial indiactor I took with my camera and macro lens in hopes that I would be able to use it to test my program out on.|Currently unused due to techical problems|
|`dial_2.jpg`|Another closeup of the same Mitutoyo dial indiactor, but this time it had a white paper behind it to help filter out the background in the program.|Currently unused due to processing times, but `dial_face.jpg` was extracted from this image|
|`dial_face.jpg`|This image is a closeup of the dial indicator face generated from `dial_2.jpg` but this is also a smaller image so it gets processed much faster which is the main reason it's used to test basically everything right now.|Actively used a lot|
|`dial_face_720p.png`|This image is basically the same as the normal `dial_face.jpg` file, except scaled to 720p due to experimenting taking a long time processing such large photos, and which basically all the program will use to test itself against from now on|