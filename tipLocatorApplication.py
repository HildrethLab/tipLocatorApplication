'''
This is the main run file for the tip locator application.
This program will run an automatic routine that locates the pipette tip for
the EHD printer in Dr. Hildreth's lab at Arizona State University.
'''

## Imports
# Built in modules
import sys # Allows interaction with system
from PyQt4 import QtGui, QtCore # Allows for the loading and control of the UI
import multiprocessing
# Custom modules
import tipLocatorUI # User interface for the application
import tipLocatorSystemController # System controller for the application
import tipLocatorParameters

def tipLocatorApplication():
    print('Application run')
    # Initializes the global parameters
    tipLocatorParameters.init()
    # Calls the UI launch function
    launchUI()

# Function to launch the UI
def launchUI():
    print('launchUI accessed')
    ## Loading and displaying the UI
    # Creates the GUI application
    print('Creating GUI application')
    app = QtGui.QApplication(sys.argv)
    # Creates the class instance defining what to display
    print('Creating an instance of the UI')
    ex = tipLocatorUI.tipLocatorUI()
    # Shows the class instance
    print('Showing the instance of the UI')
    ex.show()
    # Exits the program when the GUI application is exited
    sys.exit(app.exec_())

# Function to launch the system controller
def launchSystemController():
    ## Starting the system controller
    # Creates an instance of the system controller
    systemController = tipLocatorSystemController.systemController()
    # Creates a thread from the system controller
    systemControllerProcess = multiprocessing.Process(target=systemController.run, args=())
    # Makes the system controller thread a daemon thread
    systemControllerProcess.daemon = True
    # Starts the system controller thread
    systemControllerProcess.start()


if __name__ == '__main__':
    tipLocatorApplication()