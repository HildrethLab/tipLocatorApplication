'''
This is the main run file for the tip locator application.
This program will run an automatic routine that locates the pipette tip for
the EHD printer in Dr. Hildreth's lab at Arizona State University.
'''

# Imports
import tipLocatorParameters # Global parameters used for the entire application
import tipLocatorUI # User interface for the application
import tipLocatorSystemController # System controller for the application


import sys # Allows interaction with system
import threading # Allows for the creation of threads

from PyQt4 import QtGui, QtCore # Allows for the loading and control of the UI

def tipLocatorApplication():
    print('Application run')

    # Initalizes the global tip locator parameters
    tipLocatorParameters.init()

    # Calls the system controller launch function
    launchSystemController()

    # Calls the UI launch function
    launchUI()


# Function to launch the UI
def launchUI():
    ## Loading and displaying the UI
    # Creates the GUI application
    app = QtGui.QApplication(sys.argv)
    # Creates the class instance defining what to display
    ex = tipLocatorUI.tipLocatorUI()
    # Shows the class instance
    ex.show()
    # Exits the program when the GUI application is exited
    sys.exit(app.exec_())

# Function to launch the system controller
def launchSystemController():
    ## Starting the system controller
    # Creates an instance of the system controller
    systemController = tipLocatorSystemController.systemController()
    # Creates a thread from the system controller
    systemControllerThread = threading.Thread(target=systemController.run, args=())
    # Makes the system controller thread a daemon thread
    systemControllerThread.daemon = True
    # Starts the system controller thread
    systemControllerThread.start()


if __name__ == '__main__':
    tipLocatorApplication()