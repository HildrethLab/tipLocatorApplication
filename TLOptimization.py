'''
Optimization function of the tip locator application.
This will take the data points collected and fit them to the cone made by the laser.
The returned values will be the offset that the first point is from focal point of the cone.
'''

## Imports
# Built in modules
from numpy import array, sqrt
from scipy import optimize
# Custom modules
import TLParameters

# Optimization class
class Optimization():
    def __init__(self):
        print('Optimization class initiated')
        # Radius of the light entering the lens in mm
        self.radius = 0.5
        # Focal length of the lens in mm
        self.focalLength = 10

        # Initial guess at the solution
        self.initialGuess = array([0.0,0.0,0.0])

    # Main method that will be fun
    def optimize(self):
        print('optimize method accessed')
        # Retrieves the data points to optimize
        sourceData = self.readData()
        # Creates the function to be optimized
        costFunction = self.distanceToCone(sourceData)

        result = optimize.minimize(costFunction,self.initialGuess)

        print(result)

    # Method to read the data points
    def readData(self):
        print('readData accessed')
        # Returns the point data collected
        return ([point for point in TLParameters.kHNSCTL_dataStorageInstances])

    # Method to determine the distance to the cone
    def distanceToCone(self,point):
        print('distanceToCone accessed')

        ap = sqrt(point[0]**2 + point[2]**2)
        b = -abs(point[1])

        return (ap - (ap - self.focalLength/self.radius*b)/(1 + self.focalLength**2/self.radius**2))**2 + (b- (-self.radius/self.focalLength*ap + b)/(1+self.radius**2/self.focalLength**2))**2

    # Method to setup the cost function (objective function)
    def costFunction(self,data):
        print('costFunction accessed')

        def cost(startingPoint):
            return sum([self.distanceToCone(point + startingPoint) for point in data])
        return cost

    # Method to record history
    def recordHistory(self):
        print('recordHistory accessed')