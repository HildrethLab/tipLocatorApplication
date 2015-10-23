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
import TLEquipment
import TLParameters

class PixelCounter(TLEquipment.Equipment):
    def __init__(self,queue_SCtoPixelCounter,pipe_UItoPixel2,pixelThresholdValue,detectionType):
        # print('Pixel Counter init accessed')
        # Initializes the inherited class
        TLEquipment.Equipment.__init__(self)

        # Sets up the queue that will be used to communicate between the system controller and pixel counter
        # print('Created queue in pixel counter')
        self.queue_SCtoPixelCounter = queue_SCtoPixelCounter
        self.pipe_UItoPixel2 = pipe_UItoPixel2

        # Color of pixel program will be searching for
        # print('Set color in pixel counter')
        self.lightColor = 'red'

        # # Threshold value of interest
        # # print('Set threshold value in pixel counter')
        # self.thresholdValue = 0.56

        # Value that will be classified as a triggering event
        self.pixelTriggerValue = pixelThresholdValue

        # Type of pixel counter that is needed, scattering beginning or ending
        self.detectionType = detectionType


    # Method for counting the number of red pixels on the screen
    def run(self):
        # print('pixel counter run accessed')
        self.pipe_UItoPixel2.send('stillRunning')
        pixelSum = self.pipe_UItoPixel2.recv()

        if self.detectionType == 'begin':
            while pixelSum <= self.pixelTriggerValue:
                pixelSum = self.pipe_UItoPixel2.recv()
                self.pipe_UItoPixel2.send('stillRunning')
                # print ('There are {} pixels in the frame, looking for {} or greater.'.format(pixelSum,self.pixelTriggerValue))
        elif self.detectionType == 'end':
            while pixelSum > self.pixelTriggerValue:
                pixelSum = self.pipe_UItoPixel2.recv()
                self.pipe_UItoPixel2.send('stillRunning')
                # print ('There are {} pixels in the frame, looking for {} or greater.'.format(pixelSum,self.pixelTriggerValue))
            else:
                print('No Detection Type specified')

        # Informs the UI that a scattering event was detected
        # print('Scattering event detected at {} pixels'.format(pixelSum))
        self.pipe_UItoPixel2.send('scatteringEventDetected')

        self.queue_SCtoPixelCounter.put(pixelSum)

        # Calls a method to clear the pixel pipe of any values that were stored before the stop command was processed
        self.clearPixelQueue()

        # print('PIXEL COUNTER FINISHED CLEARING THE QUEUE')
        self.queue_SCtoPixelCounter.put('Pixel counter finished')

     # Method to remove all entries from the pixel queue
    def clearPixelQueue(self):
        # print('Starting to empty pixel count pipe')
        # Sets a continue emptying queue to true
        continueEmptyingQueue = True
        # Runs a loop until the queue is empty
        while continueEmptyingQueue:
            nextPipeValue = self.pipe_UItoPixel2.recv()
            if nextPipeValue == 'End of pixel count':
                # print('Pixel count pipe is empty')
                break
            # print('Current pixel count pipe value: {}'.format(nextPipeValue))
