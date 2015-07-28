'''
System Control module for the tip locator application.
This is the main control module that will execute tasks based on the users input
into the UI.
'''

# Imports
import tipLocatorParameters # Global parameters used for the entire application

import threading # Allows us to access thread control
import time # TEMPT FOR TESTING

# System controller class that inherits threading
class systemController(threading.Thread):
    def __init__(self):
        print('System Controller Initialized')
        # Sets the main controll loop to running = True
        tipLocatorParameters.updateParameter(tipLocatorParameters.kHNSCTL_mainControlLoopRunning,True)

    def run(self):
        print('System Controller Run')

        i = 0

        while tipLocatorParameters.retrieveParameter(tipLocatorParameters.kHNSCTL_mainControlLoopRunning):

            print('Running {}'.format(i))
            i += 1
            time.sleep(3)

    def tipLocatorRoutine(self):
        print('Tip locator routine started')

