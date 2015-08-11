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

        '''
        Initial tests just returns a random number

        # Continues checking the pixel count until told to stop
        continueCounting = True
        while continueCounting:
        # for i in range(100):
            self._queue_SCtoPixelCounter.put(random.random()*110000)
            time.sleep(.1)

        '''