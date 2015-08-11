'''
Module for the tip locator application that processes a video feed and returns the number of red pixels
currently in the frame.
'''

## Imports
# Built in modules
import SimpleCV # computer vision handler
import cv2 # Another computer vision handler
import time
import random
# Custom modules
import tipLocatorEquipment

class pixelCounter(tipLocatorEquipment.equipment):
    def __init__(self,_queue_SCtoPixelCounter):
        print('Pixel Counter init accessed')
        # Initializes the inherited class
        tipLocatorEquipment.equipment.__init__(self)

        # Sets up the queue that will be used to communicate between the system controller and pixel counter
        print('Created queue in pixel counter')
        self._queue_SCtoPixelCounter = _queue_SCtoPixelCounter

        # Color of pixel program will be searching for
        print('Set color in pixel counter')
        self.lightColor = 'red'

        # Threshold value of interest
        print('Set threshold value in pixel counter')
        self.thresholdValue = 0.90

        # Creates the display
        print('Creating display in pixel counter')
        # self.display = SimpleCV.Display()
        # Creates the camera
        print('Creating camera in pixel counter')
        self.camera = SimpleCV.Camera()

    # Method for counting the number of red pixels on the screen
    def run(self):
        print('pixel counter run accessed')

        # while self.display.isNotDone():
        for i in range(1000):
            # Creates a video feed of the camera images
            videoFeed = self.camera.getImage()
            videoFeedBlank = videoFeed * 0

            # Splits the video into three color channels in grayscale
            (redVideoChannel, greenVideoChannel, blueVideoChannel) = videoFeed.splitChannels()


            # Creates a new video feed that is a grayscale video of the specified laser color values
            if self.laserColor == 'red':
                videoFeedConverted = videoFeedBlank.mergeChannels(redVideoChannel,redVideoChannel,redVideoChannel)
                colorChannel = 0
            elif self.laserColor == 'green':
                videoFeedConverted = videoFeedBlank.mergeChannels(greenVideoChannel,greenVideoChannel,greenVideoChannel)
                colorChannel = 1
            elif self.laserColor == 'blue':
                videoFeedConverted = videoFeedBlank.mergeChannels(blueVideoChannel,blueVideoChannel,blueVideoChannel)
                colorChannel = 2

            # Thresholds the video around thresholdValue
            videoFeedConverted = videoFeedConverted.binarize(255*thresholdValue).invert()

            # Creates a matrix of values for video feed
            pixelSumMatrix = videoFeedConverted.getNumpy()
            # Counts the number of elementr in the matrix with a value greater than 0, this is then number of colored pixels
            pixelSum = cv2.countNonZero(pixelSumMatrix[:,:,0])
            print ('There are {} pixels in the frame:'.format(pixelSum))

            time.sleep(.1)

        '''
        Initial tests just returns a random number

        # Continues checking the pixel count until told to stop
        continueCounting = True
        while continueCounting:
        # for i in range(100):
            self._queue_SCtoPixelCounter.put(random.random()*110000)
            time.sleep(.1)

        '''