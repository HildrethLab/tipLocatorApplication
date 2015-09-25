'''
Program that takes a video stream and returns the number of red pixels above
the specified threshold value

'''

import SimpleCV
from scipy import ndimage
import numpy as np
import cv2
import time

processVideoRunning = True
camera = SimpleCV.Camera(0)
thresholdValue = 0.2

while processVideoRunning:
    # print('Inside processVideo loop')
    # Creates the video feed form the camera for processing
    videoFeed = camera.getImage()
    # Creates a blank video feed for merging desired channel into
    videoFeedBlank = videoFeed * 0
    # Splits the video into its three color channels
    (redVideoChannel, greenVideoChannel, blueVideoChannel) = videoFeed.splitChannels()
    # Merges the red video channel into all three color channels of blank video feed to create grayscale video
    videoFeedConverted = videoFeedBlank.mergeChannels(redVideoChannel,redVideoChannel,redVideoChannel)
    # Threasholds video based on the specified threshold value
    videoFeedConverted = videoFeedConverted.binarize(255 * thresholdValue).invert()

    # Creates a matrix of values for video feed
    pixelSumMatrix = videoFeedConverted.getNumpy()
    # Counts the number of elements in the matrix with a value greater than 0, this is the number of colored pixels
    pixelSum = cv2.countNonZero(pixelSumMatrix[:,:,0])
    print(pixelSum)
    time.sleep(.1)


'''
# Initiates the display and the camera that will be used
display = SimpleCV.Display()
camera = SimpleCV.Camera()

# Variable used to specify the color of the laser ('red','green', or 'blue')
laserColor = 'red'

# Variable used to switch between the filter and unfiltered video
unfilteredVideo = False

# Percentage of color we want to threshold around
thresholdValue = 0.90

# Creates a varible that will be updated with the number of pixels above the threshold on the screen
numberOfRedPixels = 0


while display.isNotDone():


    # Creates a video feed of the camera images
    videoFeed = camera.getImage()
    videoFeedBlank = videoFeed*0

    # Listens for a left click on the video display and ends the program if it occurs
    if display.mouseLeft:
        display.isDone()
        break
    # Listens for a right click on the video display and switches between unfiltered and filtered video
    if display.mouseRight:
        unfilteredVideo = not unfilteredVideo

    # Splits the video into the three color channels in grayscale
    (redVideoChannel, greenVideoChannel, blueVideoChannel) = videoFeed.splitChannels()

    # Creates a new video feed that is a grayscale video of the specified laser color values
    if laserColor == 'red':
        videoFeedConverted = videoFeedBlank.mergeChannels(redVideoChannel,redVideoChannel,redVideoChannel)
        colorChannel = 0
    elif laserColor == 'green':
        videoFeedConverted = videoFeedBlank.mergeChannels(greenVideoChannel,greenVideoChannel,greenVideoChannel)
        colorChannel = 1
    elif laserColor == 'blue':
        videoFeedConverted = videoFeedBlank.mergeChannels(blueVideoChannel,blueVideoChannel,blueVideoChannel)
        colorChannel = 2


    # Thresholds the video around thresholdValue
    videoFeedConverted = videoFeedConverted.binarize(255*thresholdValue).invert()

    # Creates a matrix of values for video feed
    pixelSumMatrix = videoFeedConverted.getNumpy()
    # Counts the number of elementr in the matrix with a value greater than 0, this is then number of colored pixels
    pixelSum = cv2.countNonZero(pixelSumMatrix[:,:,0])
    print ('There are {} pixels in the frame:'.format(pixelSum))

    # If statement used to specify which video feed to display
    if unfilteredVideo:
        videoFeed.save(display)
        # blueVideoChannel.save(display)
    else:
        videoFeedConverted.save(display)
        # redVideoChannel.threshold(thresholdValue).save(display)

'''