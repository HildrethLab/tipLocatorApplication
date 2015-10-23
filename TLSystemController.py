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
import datetime
import csv
# Custom modules
import TLXYZStages # Specific XPS stages
import TLPixelCounter # Method to counter number of pixels on screen
import TLParameters # Global parameters shared between the processes
import TLDataClass # Method holding the data class for the application
import TLOptimization # Method for optimizing the data collected to find the focal point of the cone

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
        self.thresholdPixelCount = 5

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

        pass

    ## Routine methods
    # Method to start the tip locator routine
    def tipLocatorRoutine(self):
        print('Tip locator routine started')
        # Clears the data storage object
        TLParameters.kHNSCTL_dataStorageInstances = []

        # Number of routine passes that will occur
        # dataPoints = 6
        # Dictionary of the max movement distance for each routine pass
        routineMovementDistances = {
            '1':[2],
            '2':[2],
            '3':[2],
            '4':[2],
            '5':[2],
            '6':[2],
            '7':[2],
            '8':[2],
            '9':[2],
            '10':[2],
            '11':[2],
            '12':[2],
            '13':[2],
            '14':[2],
            '15':[2],
            '16':[2],
            '17':[2],
            '18':[2],
            '19':[2],
            '20':[2],
            '21':[2],
            '22':[2],
            '23':[2],
            '24':[2],
            '25':[2],
            '26':[2],
            '27':[2],
            '28':[2],
            '29':[2],
            '30':[2],
            '31':[2],
            '32':[2],
            '33':[2],
            '34':[2],
            '35':[2],
            '36':[2],
        }
        # Dictionary for the movement direction for each routine pass
        routineMovementDirections = {
            '1':self.substrateStages.positioner_X,
            '2':self.substrateStages.positioner_X,
            '3':self.substrateStages.positioner_X,
            '4':self.substrateStages.positioner_X,
            '5':self.substrateStages.positioner_X,
            '6':self.substrateStages.positioner_X,
            '7':self.substrateStages.positioner_X,
            '8':self.substrateStages.positioner_X,
            '9':self.substrateStages.positioner_X,
            '10':self.substrateStages.positioner_X,
            '11':self.substrateStages.positioner_X,
            '12':self.substrateStages.positioner_X,
            '13':self.substrateStages.positioner_X,
            '14':self.substrateStages.positioner_X,
            '15':self.substrateStages.positioner_X,
            '16':self.substrateStages.positioner_X,
            '17':self.substrateStages.positioner_X,
            '18':self.substrateStages.positioner_X,
            '19':self.substrateStages.positioner_X,
            '20':self.substrateStages.positioner_X,
            '21':self.substrateStages.positioner_X,
            '22':self.substrateStages.positioner_X,
            '23':self.substrateStages.positioner_X,
            '24':self.substrateStages.positioner_X,
            '25':self.substrateStages.positioner_X,
            '26':self.substrateStages.positioner_X,
            '27':self.substrateStages.positioner_X,
            '28':self.substrateStages.positioner_X,
            '29':self.substrateStages.positioner_X,
            '30':self.substrateStages.positioner_X,
            '31':self.substrateStages.positioner_X,
            '32':self.substrateStages.positioner_X,
            '33':self.substrateStages.positioner_X,
            '34':self.substrateStages.positioner_X,
            '35':self.substrateStages.positioner_X,
            '36':self.substrateStages.positioner_X,
        }
        # Dictionary for the starting location for each routine pass
        routineStartingLocations = {
            '1':[39.4,-6,4.6],
            '2':[39.4,-6,4.6],
            '3':[39.4,-6,4.6],
            '4':[39.4,-6,4.6],
            '5':[39.4,-6,4.6],
            '6':[39.4,-6,4.6],
            '7':[39.4,-6,4.6],
            '8':[39.4,-6,4.6],
            '9':[39.4,-6,4.6],
            '10':[39.4,-6,4.6],
            '11':[39.4,-6,4.6],
            '12':[39.4,-6,4.6],
            '13':[39.4,-6,4.6],
            '14':[39.4,-6,4.6],
            '15':[39.4,-6,4.6],
            '16':[39.4,-6,4.6],
            '17':[39.4,-6,4.6],
            '18':[39.4,-6,4.6],
            '19':[39.4,-6,4.6],
            '20':[39.4,-6,4.6],
            '21':[39.4,-6,4.6],
            '22':[39.4,-6,4.6],
            '23':[39.4,-6,4.6],
            '24':[39.4,-6,4.6],
            '25':[39.4,-6,4.6],
            '26':[39.4,-6,4.6],
            '27':[39.4,-6,4.6],
            '28':[39.4,-6,4.6],
            '29':[39.4,-6,4.6],
            '30':[39.4,-6,4.6],
            '31':[39.4,-6,4.6],
            '32':[39.4,-6,4.6],
            '33':[39.4,-6,4.6],
            '34':[39.4,-6,4.6],
            '35':[39.4,-6,4.6],
            '36':[39.4,-6,4.6],
        }

        dataPoints = len(routineStartingLocations)
        # dataPoints = 1

        # Creates an instance of the stages for the routine
        routineStages = TLXYZStages.XYZStages()
        routineStages.initializeStages()

        ## Data point collection
        # Loop that runs to collect the data points
        for i in range(dataPoints):
            # Updates the stages velocity so that they move to the start position faster
            routineStages.updateStageVelocity(1)

            # Moves the stages to the starting position for each scan
            print('Moving to starting position {}'.format(i+1))
            routineStages.moveStageAbsolute(self.substrateStages.macroGroup,routineStartingLocations[str(i+1)])

            # Updates the stages velocity so that the routine is run slower
            routineStages.updateStageVelocity(0.01)

            # Creates the thread for the stages that will be moving in the routine
            # print('Starting routine stage movement')
            routineStagesThread = threading.Thread(target=routineStages.moveStageRelative, args=(routineMovementDirections[str(i+1)],routineMovementDistances[str(i+1)]))
            routineStagesThread.start()

            # #### FOR TESTING #### Checking to see the spread of the scattering detection location
            # # Moves the stages to the starting position for each scan
            # print('Moving to starting position {}'.format(1))
            # self.substrateStages.moveStageAbsolute(self.substrateStages.macroGroup,routineStartingLocations[str(1)])
            #
            # # Creates the thread for the stages that will be moving in the routine
            # print('Starting routine stage movement')
            # routineStagesThread = threading.Thread(target=routineStages.moveStageRelative, args=(routineMovementDirections[str(1)],routineMovementDistances[str(1)]))
            # routineStagesThread.start()
            # ##### END OF TESTING #####

            ### First step of the routine, find side 1
            print('STARTING STEP 1')
            # time.sleep(2)

            ## Begins scattering event detection
            # Informs the UI to start processing the video feed
            self.queue_routineLoop.put('Start video processing')
            print('Starting scattering detection begin')
            pixelTriggerValue = self.detectScatteringBegin()

            # Stops the stage movement
            routineStages.moveStageAbort()

            # Retrieving stage position
            # print('Retrieving stage position')
            [x1,y1,z1] = routineStages.retrieveStagePosition()
            print('Stage position: {},{},{}'.format(x1,y1,z1))

            # Creates a data point with the stage position, pixel count, and point type
            TLDataClass.TLData(x1,y1,z1,pixelTriggerValue,1)

            '''
            #######
            TEMP REMOVE FOR TESTING OF NEW ROUTINE
            #######

            ## Begins the vertical movement portion of the routine
            # Sets stage velocity so that the movement occurs quickly
            # print('Setting Stage Velocity to 1')
            routineStages.updateStageVelocity(1)

            # Retrieves the stage position
            [x,y,z] = routineStages.retrieveStagePosition()

            # Move the stages vertically upwards from current position
            # print('Moving the stages upward by .1 mm')
            routineStages.moveStageAbsolute(routineStages.macroGroup, [x,y,z-0.1])

            # Sets the stage velocity so that the dection occurs slowly
            # print('Setting Stage Velocity to 1')
            routineStages.updateStageVelocity(0.01)

            # Begin lowering the stages
            # print('Starting routine stage movement')
            routineStagesThread = threading.Thread(target=routineStages.moveStageRelative, args=(self.substrateStages.positioner_Z,[0.2]))
            routineStagesThread.start()

            ## Begins scattering event detection
            # Informs the UI to start processing the video feed
            self.queue_routineLoop.put('Start video processing')
            # print('Starting scattering detection')
            pixelTriggerValue = self.detectScatteringBegin()

            # Stops the stage movement
            # print('Stopping stage movement')
            routineStages.moveStageAbort()

            # Retrieving stage position
            # print('Retrieving stage position')
            [x,y,z] = routineStages.retrieveStagePosition()
            print('Stage position: {},{},{}'.format(x,y,z))

            # Creates a data point with the stage position, pixel count, and point type
            TLDataClass.TLData(x,y,z,pixelTriggerValue,2)
            '''

            ### Second step of the routine, find side 2
            print('STARTING STEP 2')
            # time.sleep(2)
            # Creates the thread for the stages that will be moving in the routine
            print('Starting second routine stage movement')
            routineStagesThread = threading.Thread(target=routineStages.moveStageRelative, args=(routineMovementDirections[str(i+1)],routineMovementDistances[str(i+1)]))
            routineStagesThread.start()

            ## Begins scattering event ending detection
            # Informs the UI to start processing the video feed
            self.queue_routineLoop.put('Start video processing')
            print('Starting scattering detection end')
            pixelTriggerValue = self.detectScatteringEnding()

            # Stops the stage movement
            routineStages.moveStageAbort()

            # Retrieving stage position
            # print('Retrieving stage position')
            [x2,y2,z2] = routineStages.retrieveStagePosition()
            print('Stage position: {},{},{}'.format(x2,y2,z2))

            # Creates a data point with the stage position, pixel count, and point type
            TLDataClass.TLData(x2,y2,z2,pixelTriggerValue,2)

            ### Third step of the rountine, split the two sides and find the top
            print('STARTING STEP 3')
            # time.sleep(2)
            # Determines the midpoint for each of the coordinates or thw first two data points
            x_mid = (x2 + x1)/2
            y_mid = (y2 + y1)/2
            z_mid = (z2 + z1)/2

            # Updates the stages velocity so that they move to the start position faster
            routineStages.updateStageVelocity(1)

            # Moves the stages to the midpoint
            print('Moving to mid position: {},{},{}'.format(x_mid,y_mid,z_mid))
            routineStages.moveStageAbsolute(self.substrateStages.macroGroup,[x_mid,y_mid,z_mid])

            # Updates the stages velocity so that they move to the start position faster
            routineStages.updateStageVelocity(0.01)

            # Begin raising the stages
            print('Starting third routine stage movement')
            routineStagesThread = threading.Thread(target=routineStages.moveStageRelative, args=(self.substrateStages.positioner_Z,[-0.5]))
            routineStagesThread.start()

            ## Begins scattering event ending detection
            # Informs the UI to start processing the video feed
            self.queue_routineLoop.put('Start video processing')
            print('Starting scattering detection end')
            pixelTriggerValue = self.detectScatteringEnding()

            # Stops the stage movement
            routineStages.moveStageAbort()

            # Retrieving stage position
            # print('Retrieving stage position')
            [x3,y3,z3] = routineStages.retrieveStagePosition()
            print('Stage position: {},{},{}'.format(x3,y3,z3))

            # Creates a data point with the stage position, pixel count, and point type
            TLDataClass.TLData(x3,y3,z3,pixelTriggerValue,3)


        # Signals the end of the routine loop
        self.queue_routineLoop.put('End routine loop')
        # Retrieves all of the data points collected
        self.retrieveDataPoints()

        # optimization = TLOptimization.Optimization()
        # optimization.optimize()

    # Method to watch for scattering event beginning
    def detectScatteringBegin(self):
        print('detectScatteringBegin accessed')
        # Creates the queues for communication with pixel counter
        queue_SCtoPixelCounter = multiprocessing.Queue()
        # Creates the pixel counter that will be used for the routine
        routinePixelCounter = TLPixelCounter.PixelCounter(queue_SCtoPixelCounter,self.pipe_UItoPixel2,self.thresholdPixelCount,'begin')
        # print('Creating video process')
        self.routinePixelCounterProcess = multiprocessing.Process(target=routinePixelCounter.run, args=())
        self.routinePixelCounterProcess.daemon = True
        # print('Starting pixel counter process')
        self.routinePixelCounterProcess.start()

        # Control loop for the tip locator routine. Runs until red pixels get above a certain number
        # print('Starting location routine')
        continueScanning = True
        while continueScanning:
            print('In routine')
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

    # Method to watch for scattering event ending
    def detectScatteringEnding(self):
        print('detectScatteringEnding accessed')
        # Creates the queues for communication with pixel counter
        queue_SCtoPixelCounter = multiprocessing.Queue()
        # Creates the pixel counter that will be used for the routine
        routinePixelCounter = TLPixelCounter.PixelCounter(queue_SCtoPixelCounter,self.pipe_UItoPixel2,self.thresholdPixelCount,'end')
        # print('Creating video process')
        self.routinePixelCounterProcess = multiprocessing.Process(target=routinePixelCounter.run, args=())
        self.routinePixelCounterProcess.daemon = True
        # print('Starting pixel counter process')
        self.routinePixelCounterProcess.start()

        # Control loop for the tip locator routine. Runs until red pixels go below a certain number
        # print('Starting location routine')
        continueScanning = True
        while continueScanning:
            # print('In routine')
            # Gets the current red pixel counter
            currentPixelCount = queue_SCtoPixelCounter.get()
            print(currentPixelCount)
            print(self.thresholdPixelCount)
            # Checks to see what the current pixel count is and ends the loop once threashold is reached
            if currentPixelCount <= self.thresholdPixelCount:
                #Threshold met, stop scanning by setting continueScanning to False
                print('Stopping because {} <= {}'.format(currentPixelCount,self.thresholdPixelCount))
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
    # Method to move the stages to the start position (not determined yet so (0,0,-5)
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

        # Changes the stage velocity
        stageInstance.updateStageVelocity(1)

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

        # Changes the stage velocity
        stageInstance.updateStageVelocity(0.1)

    # Method to shut down the system controller
    def shutDown(self):
        # Tries to close any processes that may be open
        self.routinePixelCounterProcess.terminate()

    # Method to retrieve all of the data points
    def retrieveDataPoints(self):

        # Opens the data file to be writen too
        dataFile = open('data/testData - ' + str(datetime.datetime.now()) + '.csv','wt')
        # Creates csv writer
        dataWriter = csv.writer(dataFile)

        # Writes the headers
        dataWriter.writerow(('x','y','z','Pixel Trigger Value','Point Type'))

        for dataSet in TLParameters.kHNSCTL_dataStorageInstances:
            print ('Current coordinate points collected: {}, {}, {} with {} pixels triggering the event. Point type: {}'.format(dataSet.x, dataSet.y, dataSet.z,dataSet.pixelTriggerValue,dataSet.pointType))
            dataWriter.writerow((dataSet.x,dataSet.y,dataSet.z,dataSet.pixelTriggerValue,dataSet.pointType))

        dataFile.close()