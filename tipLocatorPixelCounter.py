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
import tipLocatorParameters

class pixelCounter(tipLocatorEquipment.equipment):
    def __init__(self,queue_SCtoPixelCounter,pipe_UItoPixel2):
        print('Pixel Counter init accessed')
        # Initializes the inherited class
        tipLocatorEquipment.equipment.__init__(self)

        # Sets up the queue that will be used to communicate between the system controller and pixel counter
        print('Created queue in pixel counter')
        self.queue_SCtoPixelCounter = queue_SCtoPixelCounter
        self.pipe_UItoPixel2 = pipe_UItoPixel2

        # Color of pixel program will be searching for
        print('Set color in pixel counter')
        self.lightColor = 'red'

        # Threshold value of interest
        print('Set threshold value in pixel counter')
        self.thresholdValue = 0.90

        # Value that will be classified as a triggering event
        self.pixelTriggerValue = 100000


    # Method for counting the number of red pixels on the screen
    def run(self):
        print('pixel counter run accessed')
        self.pipe_UItoPixel2.send('stillRunning')
        pixelSum = self.pipe_UItoPixel2.recv()
        while pixelSum <= self.pixelTriggerValue:
            pixelSum = self.pipe_UItoPixel2.recv()
            self.pipe_UItoPixel2.send('stillRunning')
            # print ('There are {} pixels in the frame, looking for {} or greater.'.format(pixelSum,self.pixelTriggerValue))

        print('Scattering event detected at {} pixels'.format(pixelSum))
        self.pipe_UItoPixel2.send('scatteringEventDetected')
        self.queue_SCtoPixelCounter.put(pixelSum)


        '''
        Initial tests just returns a random number

        # Continues checking the pixel count until told to stop
        continueCounting = True
        while continueCounting:
        # for i in range(100):
            self._queue_SCtoPixelCounter.put(random.random()*110000)
            time.sleep(.1)

        '''