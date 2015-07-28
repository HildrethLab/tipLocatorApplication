'''
Tip Locator application UI module that inherits the base tip locator UI.
The base module is the one directly created by pyuic4 in terminal.
This module has all of the functionality for the UI
'''

# Imports
import tipLocatorUIBase # Base UI that will be inherited
import tipLocatorParameters # Global parameters for the application

from PyQt4 import QtGui, QtCore # Allows for the use of PyQt funtionality
import sys # Allows interaction with system

# Primary UI class that inherits from the base UI
class tipLocatorUI(tipLocatorUIBase.Ui_TipLocator):
    def __init__(self):
        # Initializes the QWidget superclass
        QtGui.QWidget.__init__(self)
        # Runs setupIU method upon initialization
        self.setupUi(self)
        # Runs the button functionality
        self.buttonFunctionality()

        # Moves the UI to the top left corner of the screen
        self.move(0,0)

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

    # Method for when a manual movement button is clicked
    def buttonClickedManualMove(self, direction, value):
        print('Manual move button clicked: Moved {} in {}'.format(value,direction))

    # Method for when an abort button is clicked
    def abortAll(self):
        print('Abort button clicked')
        try:
            print('Ending main control loop')
            tipLocatorParameters.updateParameter(tipLocatorParameters.kHNSCTL_mainControlLoopRunning,False)
        except:
            print('Failed to abort')

    # Method for when the tip locator routine button is clicked
    def startTipLocatorRoutine(self):
        print('Tip locator routine start button clicked')

    # Method for when the initial position button is clicked
    def moveToInitialPosition(self):
        print('Tip locator move to initial position button clicked')

    # Method for starting the system controller

# Main function that loads and runs the UI for testing
def tipLocatorApplicationMain():
    # Creates the GUI application
    app = QtGui.QApplication(sys.argv)
    # Creates the class instance defining what to display
    ex = tipLocatorUI()
    # Shows the class instance
    ex.show()
    # Exits the program when the GUI application is exited
    sys.exit(app.exec_())

if __name__ == '__main__':
    tipLocatorApplicationMain()