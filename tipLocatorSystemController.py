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
import tipLocatorXYZStages # Specific XPS stages
import tipLocatorPixelCounter # Method to counter number of pixels on screen
import tipLocatorParameters # Global parameters shared between the threads

# System controller class that inherits threading
class systemController():
    def __init__(self,queue_SCtoUI,pipe_UItoPixel2):
        print('System Controller Initialized')
        # Creates the instance's queue connection with the UI
        self.queue_SCtoUI = queue_SCtoUI
        self.pipe_UItoPixel2 = pipe_UItoPixel2

        # Creates the dictionary of commands
        self._commandList = {
            'startTipLocatorRoutine' : self.tipLocatorRoutine,
            'finishedTipLocatorRoutine' : self.tipLocatorRoutineFinished,
            'stopTipLocatorRoutine' : self.abortRoutine,
            'moveStagesToInitialPosition' : self.moveStageToInitialPosition,
            'moveStagesRelative' : self.moveStagesRelative,
            'abortRoutine' : self.abortRoutine(),
            'shutDown' : self.shutDown()
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
        self.thresholdPixelCount = 100000

    ## Method to run the system controller loop
    # The loop is always running and responds based on the commands received from the pipe
    def run(self):
        print('System Controller Run')

        # Initializes the equipment
        print('Initializing Equipment')
        self.initializeEquipment()
        # Primary system controller loop that is always running
        while True:
            # Checks to see if there queue is empty, if not gets the command
            # print('Checking for items in queue')
            if not self.queue_SCtoUI.empty():
                # Gets the next command from the queue
                _command = self.queue_SCtoUI.get()
                print('Received command {}'.format(_command))
                try:
                    # Tries to run the method associated with the command received
                    self._commandList[_command]()
                except:
                    print('Unknown command issued: {}'.format(_command))
            # Delay between each check of the queue
            time.sleep(1)

    ## Initialization methods
    # Initializes the equipment
    def initializeEquipment(self):
        # Creates the visa resource manager

        # Creates the stages
        self.substrateStages = tipLocatorXYZStages.XYZStages()
        # Initializes the stages
        self.substrateStages.initializeStages()

    ## Routine methods
    # Method to start the tip locator routine
    def tipLocatorRoutine(self):
        print('Tip locator routine started')
        # Creates the queues for communication with pixel counter and stages
        queue_SCtoStages = multiprocessing.Queue()
        queue_SCtoPixelCounter = multiprocessing.Queue()

        # Creates and initializes the stages for the routine
        routineStagesInstance = tipLocatorXYZStages.XYZStages()
        routineStagesInstance.initializeStages()

        # Creates the pixel counter that will be used for the routine
        routinePixelCounter = tipLocatorPixelCounter.pixelCounter(queue_SCtoPixelCounter,self.pipe_UItoPixel2)
        print('Creating video process')
        self.routinePixelCounterProcess = multiprocessing.Process(target=routinePixelCounter.run, args=())
        self.routinePixelCounterProcess.daemon = True
        print('Starting pixel counter process')
        self.routinePixelCounterProcess.start()

        # Creates a new process holding the stages and starts them moving
        locatorRoutineStages = tipLocatorXYZStages.XYZStages()
        locatorRoutineStages.initializeStages()
        locatorRoutineStagesProcess = multiprocessing.Process(target=locatorRoutineStages.moveStageRelative, args=(locatorRoutineStages.positioner_Y,10.0))
        locatorRoutineStagesProcess.daemon = True
        locatorRoutineStagesProcess.start()
        # Control loop for the tip locator routine. Runs until red pixels get above a certain number
        print('Starting location routine')
        continueScanning = True
        while continueScanning:
            print('In routine')
            # Gets the current red pixel counter
            currentPixelCount = queue_SCtoPixelCounter.get()
            # Checks to see what the current pixel count is and ends the loop once it is reached
            if currentPixelCount >= self.thresholdPixelCount:
                #Threshold met, stop scanning by setting continueScanning to False
                continueScanning = False
            print('End of loop Count:{}'.format(currentPixelCount))
        print('Location found')
        locatorRoutineStages.moveStageAbort()
        currentStageLocation = locatorRoutineStages.retrieveStagePostion()
        locatorRoutineStagesProcess.terminate()
        print(currentStageLocation)

        print('Scattering event triggered at {} pixels'.format(currentPixelCount))

    # Method to close pixel counter process once routine is finished
    def tipLocatorRoutineFinished(self):
        print('tipLocatorRoutineFinished accessed')
        self.routinePixelCounterProcess.terminate()

    # Method to abord the routine
    def abortRoutine(self):
        print('abortRoutine accessed')

    ## Movement commands
    # Method to move the stages to the start position (not determined yet so (0,0,0)
    def moveStageToInitialPosition(self):
        print('moveStagesToOrigin accessed')
        # Sends absolute movement command to stages
        self.substrateStages.moveStageAbsolute(self.substrateStages.macroGroup,[0.0,0.0,0.0])

    # Method to move the stages to a relative location
    def moveStagesRelative(self):
        print('moveStagesRelative accessed')
        # Pulls the movement direction from the UI / system controller queue
        direction = self.queue_SCtoUI.get()
        # Pulls the movement distance from the UI / system controller queue
        distance = self.queue_SCtoUI.get()

        # Creates an instance of the stages to use for relative movement
        stageInstance = tipLocatorXYZStages.XYZStages()
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
        print('Creating movement process')
        movementProcess = multiprocessing.Process(target=stageInstance.moveStageRelative,args=(direction,[distance * directionMultiplier]))
        print('Starting movement process')
        movementProcess.start()
        print('Finished movement process')

    # Method to shut down the system controller
    def shutDown(self):
        # Tries to close any processes that may be open
        try:
            self.routinePixelCounterProcess.terminate()
        except:
            print('Failed to shut down all processes')

