'''
System Control module for the tip locator application.
This is the main control module that will execute tasks based on the users input
into the UI.
'''

## Imports
# Built in modules
import multiprocessing # Allows us to access process controls
import threading # Allows for the usage of threads (TESTING)
import time # TEMPT FOR TESTING
# Custom modules
import TLXYZStages # Specific XPS stages
import TLPixelCounter # Method to counter number of pixels on screen
import TLParameters # Global parameters shared between the processes
import TLDataClass # Method holding the data class for the application

# System controller class that inherits threading
class SystemController():
    def __init__(self,queue_SCtoUI,queue_routineLoop,pipe_UItoPixel2):
        # print('System Controller Initialized')
        # Creates the instance's queue connection with the UI
        self.queue_SCtoUI = queue_SCtoUI
        self.queue_routineLoop = queue_routineLoop
        self.pipe_UItoPixel2 = pipe_UItoPixel2

        # Creates the dictionary of commands
        self._commandList = {
            'startTipLocatorRoutine' : self.tipLocatorRoutine,
            'finishedTipLocatorRoutine' : self.tipLocatorRoutineFinished,
            'stopTipLocatorRoutine' : self.abortRoutine,
            'moveStagesToInitialPosition' : self.moveStageToInitialPosition,
            'moveStagesRelative' : self.moveStagesRelative,
            'abortRoutine' : self.abortRoutine,
            'shutDown' : self.shutDown
        }

        # Creates the dictionary of movement direction (multiplier for movement distance)
        self._movementDirectionDictionary = {
            '+X' : 1,
            '-X' : -1,
            '+Y' : 1,
            '-Y' : -1,
            '+Z' : 1,
            '-Z' : -1
        }

        # Sets the desired number of pixels threshold that will trigger the scattering event
        self.thresholdPixelCount = 400000

    ## Method to run the system controller loop
    # The loop is always running and responds based on the commands received from the pipe
    def run(self):
        # print('System Controller Run')

        # Initializes the equipment
        # print('Initializing Equipment')
        self.initializeEquipment()
        # Primary system controller loop that is always running
        while True:
            # Checks to see if there queue is empty, if not gets the command
            # print('Checking for items in queue')

            if not self.queue_SCtoUI.empty():
                print('Attempting to retrieve command from queue')
                # Gets the next command from the queue
                _command = self.queue_SCtoUI.get()
                print('Received command {}'.format(_command))
                self._commandList[_command]()

    ## Initialization methods
    # Initializes the equipment
    def initializeEquipment(self):
        # Creates the stages
        self.substrateStages = TLXYZStages.XYZStages()
        # Initializes the stages
        self.substrateStages.initializeStages()

    ## Routine methods
    # Method to start the tip locator routine
    def tipLocatorRoutine(self):
        print('Tip locator routine started')
        # Specifies max distance to move the stages while looking for a scattering event
        routineMovementDistance = 5.0
        dataPoints = 6

        ## Data point collection
        # Loop that runs 6 times to collect 6 data points
        for i in range(dataPoints):
            # print('Collecting data point {}'.format(i))
            # Initializing stage movement
            # Sends the movement direction to the queue to be read
            # print('Sending direction to queue')
            self.queue_SCtoUI.put('+Y')
            # Sends the movement distance to the queue to be read
            # print('Sending distance to queue')
            self.queue_SCtoUI.put(routineMovementDistance)
            # Calls the relative stage movement method
            # print('Calling movement method')
            self.moveStagesRelative()

            ## Begins scattering event detection
            # Informs the UI to start processing the video feed
            self.queue_routineLoop.put('Start video processing')
            # print('Starting scattering detection')
            pixelTriggerValue = self.detectScatteringEvent()



            print("SCATTERING EVENT")

            time.sleep(3)

            # Stopping stage movement
            # print('Stopping stage movement')
            # stages.moveStageAbort()
            # Retrieving stage position
            print('Retrieving stage position')
            [x,y,z] = self.substrateStages.retrieveStagePosition()
            print('Stage position: {},{},{}'.format(x,y,z))



            # Creates a data point with the stage position and pixel coiunt
            TLDataClass.TLData(x,y,z,pixelTriggerValue)

        # Signals the end of the routine loop
        self.queue_routineLoop.put('End routine loop')
        # Retrieves all of the data points collected
        self.retrieveDataPoints()

    # Method to watch for scattering event
    def detectScatteringEvent(self):
        # print('detectScatteringEvent accessed')
        # Creates the queues for communication with pixel counter
        queue_SCtoPixelCounter = multiprocessing.Queue()
        # Creates the pixel counter that will be used for the routine
        routinePixelCounter = TLPixelCounter.PixelCounter(queue_SCtoPixelCounter,self.pipe_UItoPixel2,self.thresholdPixelCount)
        # print('Creating video process')
        self.routinePixelCounterProcess = multiprocessing.Process(target=routinePixelCounter.run, args=())
        self.routinePixelCounterProcess.daemon = True
        # print('Starting pixel counter process')
        self.routinePixelCounterProcess.start()

        # Control loop for the tip locator routine. Runs until red pixels get above a certain number
        # print('Starting location routine')
        continueScanning = True
        while continueScanning:
            # print('In routine')
            # Gets the current red pixel counter
            currentPixelCount = queue_SCtoPixelCounter.get()
            # Checks to see what the current pixel count is and ends the loop once threashold is reached
            if currentPixelCount >= self.thresholdPixelCount:
                #Threshold met, stop scanning by setting continueScanning to False
                continueScanning = False
            print('End of loop Count:{}'.format(currentPixelCount))
        print('Location found')
        if queue_SCtoPixelCounter.get() == 'Pixel counter finished':
            print('Received confirmation that pixel counter is finished')
            self.routinePixelCounterProcess.terminate()

        # Returns the number of pixels that triggered the event
        return currentPixelCount

    # Method to close pixel counter process once routine is finished
    def tipLocatorRoutineFinished(self):
        print('tipLocatorRoutineFinished accessed')
        self.routinePixelCounterProcess.terminate()

    # Method to abory the routine
    def abortRoutine(self):
        print('abortRoutine accessed')
        print('retrieveStagePosition accessed - SC')
        self.substrateStages.moveStageAbort()

    ## Movement commands
    # Method to move the stages to the start position (not determined yet so (0,0,0)
    def moveStageToInitialPosition(self):
        print('moveStagesToOrigin accessed')
        # Sends absolute movement command to stages
        self.substrateStages.moveStageAbsolute(self.substrateStages.macroGroup,[0.0,0.0,-5.0])

    # Method to retreive the stage position
    def retrieveStagePosition(self):
        print('retrieveStagePosition accessed - SC')
        # Sends request for stage position to stages
        [x,y,z] = self.substrateStages.retrieveStagePosition()
        print(x,y,z)
        return(x,y,z)


    # Method to move the stages to a relative location
    def moveStagesRelative(self):
        print('moveStagesRelative accessed')
        # Pulls the movement direction from the UI / system controller queue
        direction = self.queue_SCtoUI.get()
        # Pulls the movement distance from the UI / system controller queue
        distance = self.queue_SCtoUI.get()

        print('Moving stages in {} by {}'.format(direction,distance))

        # Creates an instance of the stages to use for relative movement
        stageInstance = TLXYZStages.XYZStages()
        stageInstance.initializeStages()

        # Determines the direction multiplier based on the direction sent
        directionMultiplier = self._movementDirectionDictionary[direction]

        # Pulls the correct direction name for the stages based on the direction of movement
        if (direction == '-X') or (direction == '+X'):
            direction = stageInstance.positioner_X
        elif (direction == '-Y') or (direction == '+Y'):
            direction = stageInstance.positioner_Y
        elif (direction == '-Z') or (direction == '+Z'):
            direction = stageInstance.positioner_Z


        # Sends relative movement command to stages on a new process
        # print('Creating movement process')
        movementProcess = threading.Thread(target=stageInstance.moveStageRelative,args=(direction,[distance * directionMultiplier]))
        # print('Starting movement process')
        movementProcess.start()
        # print('Finished movement process')

        # Test control loop to stop stage movement
        number = 0
        while True:
            print('loop {}'.format(number))
            if number > 5:
                print('STOPPING STAGE MOVEMENT')
                stageInstance.moveStageAbort()
                break
            number += 1
            time.sleep(.25)

    # Method to shut down the system controller
    def shutDown(self):
        # Tries to close any processes that may be open
        self.routinePixelCounterProcess.terminate()

    # Method to retrieve all of the data points
    def retrieveDataPoints(self):

        for dataSet in TLParameters.kHNSCTL_dataStorageInstances:
            print ('Current coordinate points collected: {}, {}, {} with {} pixels triggering the event.'.format(dataSet.x, dataSet.y, dataSet.z,dataSet.pixelTriggerValue))