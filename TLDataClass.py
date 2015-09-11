'''
Data class for the tip locator application.
This module will be imported and then an instance of the class will be created for each of the
data points collected during the tip locating routine.
'''

## Imports
# Built in modules

# Custom modules
import TLParameters

# Defines the tip locator data class. This class stores the x,y,z stage locator whenever a scattering event occurs.
class TLData():
    def __init__(self,x,y,z,pixelTriggerValue):
        self.x = x
        self.y = y
        self.z = z
        self.pixelTriggerValue = pixelTriggerValue

        # Adds the instance to the global list of the instances
        TLParameters.updateDataStorageInstances(self)