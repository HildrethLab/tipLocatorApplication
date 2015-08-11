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
# Custom modules
import tipLocatorUIBase # Base UI that will be inherited
import tipLocatorSystemController # System controller class

# Primary UI class that inherits from the base UI
class tipLocatorUI(tipLocatorUIBase.Ui_TipLocator):
    def __init__(self):
        # Initializes the QWidget superclass
        QtGui.QWidget.__init__(self)
        # Runs setupIU method upon initialization
        self.setupUi(self)
        # Runs the button functionality
        self.buttonFunctionality()

        # Creates the pipe for communicating with the system controller
        self._queue_SCtoUI = multiprocessing.Queue()

        # Moves the UI to the top left corner of the screen
        self.move(0,0)

        # Initializes the system controller
        self.initializeSystemController(self._queue_SCtoUI)

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
        # Attempts to close the system controller process and then quit the application
        try:
            self.systemControllerProcess.terminate()
            print('System Controller Process terminated')
        except:
            print('Failed to shutdown system controller process')
        sys.exit()

    # Method for when a manual movement button is clicked
    def buttonClickedManualMove(self, _direction, _value):
        print('Manual move button clicked: Moved {} in {}'.format(_value,_direction))
        # Attempts to write moveStagesRelative to system controller queue
        try:
            print('Attempting to send move stages relative command')
            self._queue_SCtoUI.put('moveStagesRelative')
            self._queue_SCtoUI.put(_direction)
            self._queue_SCtoUI.put(_value)
        except:
            print('Failed to move stages relative')


    # Method for when an abort button is clicked
    def abortAll(self):
        print('Abort button clicked')
        # Attempts to write stopTipLocatorRoutine to system controller queue
        try:
            print('Ending main control loop')
            self._queue_SCtoUI.put('abortRoutine')
            self._queue_SCtoUI.put('stopTipLocatorRoutine')
        except:
            print('Failed to abort')

    # Method for when the tip locator routine button is clicked
    def startTipLocatorRoutine(self):
        print('Tip locator routine start button clicked')
        # Attempts to write startTipLocatorRoutine to system controller queue
        try:
            print('Starting main routine')
            self._queue_SCtoUI.put('startTipLocatorRoutine')
        except:
            print('Main routine failed to start')

    # Method for when the initial position button is clicked
    def moveToInitialPosition(self):
        print('Tip locator move to initial position button clicked')
        # Attempts to write moveStagesToInitialPosition to system controller queue
        try:
            print('UI sending move to initial position command')
            self._queue_SCtoUI.put('moveStagesToInitialPosition')
        except:
            print('Failed to move stages to initial position')

    # Method for starting the system controller
    def initializeSystemController(self,_queue_SCtoUI):
        print('initializeSystemController accessed')
        ## Starting the system controller
        # Creates an instance of the system controller
        print('Creating system controller')
        self.systemController = tipLocatorSystemController.systemController(_queue_SCtoUI)
        # Creates a thread from the system controller
        print('Creating process for system controller')
        self.systemControllerProcess = multiprocessing.Process(target=self.systemController.run, args=())
        # Makes the system controller thread a not daemon process so it can spawn additional processes
        print('Setting system controller process as not daemon')
        self.systemControllerProcess.daemon = False
        # Starts the system controller thread
        print('Starting the system controller process')
        self.systemControllerProcess.start()

# Main function that loads and runs the UI for testing
def tipLocatorApplicationMain():
    print('tipLocatorApplicationMain accessed')
    ## Loading and displaying the UI
    # Creates the GUI application
    print('Creating GUI application')
    app = QtGui.QApplication(sys.argv)
    # Creates the class instance defining what to display
    print('Creating an instance of the UI')
    ex = tipLocatorUI()
    # Shows the class instance
    print('Showing the instance of the UI')
    ex.show()
    # Exits the program when the GUI application is exited
    sys.exit(app.exec_())

if __name__ == '__main__':
    tipLocatorApplicationMain()