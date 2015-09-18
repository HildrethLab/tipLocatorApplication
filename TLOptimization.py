'''
Optimization function of the tip locator application.
This will take the data points collected and fit them to the cone made by the laser.
The returned values will be the offset that the first point is from focal point of the cone.
'''

## Imports
# Built in modules

# Custom modules
import TLParameters

# Optimization class
class Optimization():
    def __init__(self):
        print('Optimization class initiated')

    # Main method that will be fun
    def optimize(self):
        print('optimize method accessed')
        sourceData, shift = self.readData()

    # Method to read the data points
    def readData(self):
        print('readData accessed')

    # Method to determine the distance to the cone
    def distanceToCone(self):
        print('distanceToCone accessed')

    # Method to setup the cost function (objective function)
    def costFunction(self):
        print('costFunction accessed')

    # Method to record history
    def recordHistory(self):
        print('recordHistory accessed')