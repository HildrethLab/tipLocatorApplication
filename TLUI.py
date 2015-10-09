'''
Tip Locator application UI module that inherits the base tip locator UI.
The base module is the one directly created by pyuic4 in terminal.
This module has all of the functionality for the UI
'''

## Imports
# Built in modules
from PyQt4 import QtGui, QtCore # Allows for the use of PyQt functionality
import sys # Allows interaction with system
import multiprocessing # Allows access to processes and their commands
import threading
import SimpleCV
import cv2
import time
# Custom modules
import TLUIBase # Base UI that will be inherited
import TLSystemController # System controller class
import TLParameters

# Primary UI class that inherits from the base UI
class TLUI(TLUIBase.Ui_TipLocator):
    def __init__(self):
        # Initializes the QWidget superclass
        QtGui.QWidget.__init__(self)
        # Runs setupIU method upon initialization
        self.setupUi(self)
        # Runs the button functionality
        self.buttonFunctionality()

        # Creates the queues for communicating between processes
        self.queue_SCtoUI = multiprocessing.Queue()
        self.queue_routineLoop = multiprocessing.Queue()
        (self.pipe_UItoPixel1,self.pipe_UItoPixel2) = multiprocessing.Pipe()

        # Moves the UI to the top left corner of the screen
        self.move(0,0)

        # Initializes the system controller
        self.initializeSystemController(self.queue_SCtoUI,self.queue_routineLoop,self.pipe_UItoPixel2)

        # Creates a camera that will be used for video processing
        self.camera = SimpleCV.Camera(0)
        # Desired threshold value for processing the video
        self.thresholdValue = 0.2

    # Method to add functionality to the UIs buttons
    def buttonFunctionality(self):
        ## Tip Locator Buttons
        # Abort button
        self.buttonTipLocatorAbortRoutine.clicked.connect(self.abortAll)

        # Initial position button
        self.buttonTipLocatorInitialPositon.clicked.connect(self.moveToInitialPosition)

        # Start routine button
        self.buttonTipLocatorStartRoutine.clicked.connect(self.startTipLocatorRoutine)

        ## Stage Control Buttons
        # Abort button
        self.buttonMovementAbort.clicked.connect(self.abortAll)

        # Manual movement buttons
        self.buttonDirectionNeg_X.clicked.connect(lambda: self.buttonClickedManualMove('-X',float(self.entryBoxDirection_X.text())))
        self.buttonDirectionNeg_Y.clicked.connect(lambda: self.buttonClickedManualMove('-Y',float(self.entryBoxDirection_Y.text())))
        self.buttonDirectionNeg_Z.clicked.connect(lambda: self.buttonClickedManualMove('-Z',float(self.entryBoxDirection_Z.text())))
        self.buttonDirectionPos_X.clicked.connect(lambda: self.buttonClickedManualMove('+X',float(self.entryBoxDirection_X.text())))
        self.buttonDirectionPos_Y.clicked.connect(lambda: self.buttonClickedManualMove('+Y',float(self.entryBoxDirection_Y.text())))
        self.buttonDirectionPos_Z.clicked.connect(lambda: self.buttonClickedManualMove('+Z',float(self.entryBoxDirection_Z.text())))

        ## System control buttons
        # Quit button
        self.buttonQuit.clicked.connect(self.buttonClickedQuit)

    # Method for when the quit button is clicked
    def buttonClickedQuit(self):
        print('Quit button clicked')
        # Attempts to close the application smoothly
        try:
            # Sends shut down command to system controller
            self.queue_SCtoUI.put('shutDown')
            # Ends the camera
            self.camera = None
            # # Ends the system controller process
            # self.systemControllerProcess.terminate()
            # print('Processes terminated')
        except:
            print('Failed to shutdown system controller process')
        sys.exit()

    # Method for when a manual movement button is clicked
    def buttonClickedManualMove(self, _direction, _value):
        # print('Manual move button clicked: Moved {} in {}'.format(_value,_direction))
        # Attempts to write moveStagesRelative to system controller queue
        try:
            # print('Attempting to send move stages relative command')
            self.queue_SCtoUI.put('moveStagesRelative')
            self.queue_SCtoUI.put(_direction)
            self.queue_SCtoUI.put(_value)
        except:
            print('Failed to move stages relative')


    # Method for when an abort button is clicked
    def abortAll(self):
        print('Abort button clicked')
        # Attempts to write stopTipLocatorRoutine to system controller queue
        try:
            print('Ending main control loop')
            self.queue_SCtoUI.put('abortRoutine')
            self.queue_SCtoUI.put('stopTipLocatorRoutine')
        except:
            print('Failed to abort')

    # Method for when the tip locator routine button is clicked
    def startTipLocatorRoutine(self):
        print('Tip locator routine start button clicked')
        # Attempts to write startTipLocatorRoutine to system controller queue
        try:
            print('Starting main routine')
            self.queue_SCtoUI.put('startTipLocatorRoutine')
        except:
            print('Main routine failed to start')

        # Sets variable used to keep routine running until complete
        routineRunning = True

        # Pauses before beginning the routine loop
        # Main tip locator routine
        while routineRunning:
            # print('Routine loop')
            QtGui.QApplication.processEvents()
            if not self.queue_routineLoop.empty():
                command = self.queue_routineLoop.get()
                print('Command received by the UI: {}'.format(command))

                if command == 'Start video processing':
                    # print('Starting to process video feed')
                    self.processVideo()
                    # print('Finished processing video')

                elif command == 'End routine loop':
                    # print('Ending routine loop')
                    routineRunning = False
            # print('Sending movement command')
            time.sleep(.5)

    # Method for when the initial position button is clicked
    def moveToInitialPosition(self):
        print('Tip locator move to initial position button clicked')
        # Attempts to write moveStagesToInitialPosition to system controller queue
        try:
            print('UI sending move to initial position command')
            self.queue_SCtoUI.put('moveStagesToInitialPosition')
        except:
            print('Failed to move stages to initial position')

    # Method for starting the system controller
    def initializeSystemController(self,queue_SCtoUI,queue_routineLoop,pipe_UItoPixel2):
        # print('initializeSystemController accessed')
        ## Starting the system controller
        # Creates an instance of the system controller
        # print('Creating system controller')
        self.systemController = TLSystemController.SystemController(queue_SCtoUI,queue_routineLoop,pipe_UItoPixel2)
        # Creates a thread from the system controller
        # print('Creating process for system controller')
        self.systemControllerProcess = threading.Thread(target=self.systemController.run, args=())
        # Makes the system controller thread a not daemon process so it can spawn additional processes
        # print('Setting system controller process as not daemon')
        self.systemControllerProcess.daemon = True
        # Starts the system controller thread
        # print('Starting the system controller process')
        self.systemControllerProcess.start()

    # Method for processing the video feed
    def processVideo(self):
        # print('processVideo accessed')
        # Sets the video processing loop variable to true
        processVideoRunning = True
        # Creates a camera that will be used to capture the video feed
        # camera = SimpleCV.Camera()
        # print('Starting processVideo loop')
        # While loop for processing the video feed
        while processVideoRunning:
            # print('Inside processVideo loop')
            # Command to manually process GUI events each iteration of the control loop
            QtGui.QApplication.processEvents()
            # Creates the video feed form the camera for processing
            videoFeed = self.camera.getImage()
            # Creates a blank video feed for merging desired channel into
            videoFeedBlank = videoFeed * 0
            # Splits the video into its three color channels
            (redVideoChannel, greenVideoChannel, blueVideoChannel) = videoFeed.splitChannels()
            # Merges the red video channel into all three color channels of blank video feed to create grayscale video
            videoFeedConverted = videoFeedBlank.mergeChannels(redVideoChannel,redVideoChannel,redVideoChannel)
            # Threasholds video based on the specified threshold value
            videoFeedConverted = videoFeedConverted.binarize(255 * self.thresholdValue).invert()

            # Creates a matrix of values for video feed
            pixelSumMatrix = videoFeedConverted.getNumpy()
            # Counts the number of elements in the matrix with a value greater than 0, this is the number of colored pixels
            pixelSum = cv2.countNonZero(pixelSumMatrix[:,:,0])
            # Sends the number of pixels counted down the UI to pixel pipe
            # print(pixelSum)
            self.pipe_UItoPixel1.send(pixelSum)
            # Checks to see if a scattering event detected message has been received and ends video processing loop if it has

            commandFromPixel = self.pipe_UItoPixel1.recv()
            # print('Command received from pixel process: {}'.format(commandFromPixel))

            if commandFromPixel == 'scatteringEventDetected':
                print('UI received command to stop processing video')
                processVideoRunning = False


        # Sends a final message down the pipe to show it is the end of the video processing (used to clear the pipe)
        # print('Sending end of pixel count command')
        self.pipe_UItoPixel1.send('End of pixel count')
        # print('Done processing video')

# Main function that loads and runs the UI for testing
def tipLocatorApplicationMain():
    # print('tipLocatorApplicationMain accessed')
    ## Loading and displaying the UI
    # Creates the GUI application
    # print('Creating GUI application')
    app = QtGui.QApplication(sys.argv)
    # Creates the class instance defining what to display
    # print('Creating an instance of the UI')
    ex = TLUI()
    # Shows the class instance
    # print('Showing the instance of the UI')
    ex.show()
    # Exits the program when the GUI application is exited
    sys.exit(app.exec_())

if __name__ == '__main__':
    tipLocatorApplicationMain()