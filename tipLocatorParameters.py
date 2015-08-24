'''
Global parameters that will be used for the tip lcoator application.
This includes the shared information between threads as well as the variables that will be used to control the
system loops
'''

## Imports
# Built in modules
import SimpleCV
import cv2
# Custom modules

# Key variables (kHNSCTL aka: key Hildreth Nano System Controller Tip Locator)
kHNSCTL_mainControlLoopRunning = 'kHNSCTL_mainControlLoopRunning'


# Function that initializes the global parameters
def init():
    # print('Parameters initialized')
    global _globalParameters
    # Creates an empty dictionary that will be updated and retrieved from
    _globalParameters = {}


# Function that updates a parameter
def updateParameter(key,value):
    global _globalParameters

    _globalParameters[key] = value

# Function that removes a parameter
def removeParameter(key):
    # global _globalParameters

    del _globalParameters[key]

# Function that retrieves a parameter
def retrieveParameter(key):
    # global _globalParameters

    return _globalParameters[key]

def listParameters():
    print (_globalParameters.keys())