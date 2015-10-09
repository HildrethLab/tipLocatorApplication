'''
Optimization function of the tip locator application.
This will take the data points collected and fit them to the cone made by the laser.
The returned values will be the offset that the first point is from focal point of the cone.
'''

## Imports
# Built in modules
from numpy import array, sqrt
from scipy import optimize
import time
# Custom modules
import TLParameters
import TLDataClass

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

        # print('sourceData:')
        # print(sourceData)
        # Creates the function to be optimized
        costFunction = self.costFunction(sourceData)

        result = optimize.minimize(costFunction,self.initialGuess)

        print(result)

    # Method to read the data points
    def readData(self):
        print('readData accessed')
        # Returns the point data collected
        # Creates a blank point object
        point = []

        # Cycles through the collected data and appends the coordinates to the point object
        for i in range(len(TLParameters.kHNSCTL_dataStorageInstances)):
            pointArray = array([TLParameters.kHNSCTL_dataStorageInstances[i].x,TLParameters.kHNSCTL_dataStorageInstances[i].y,TLParameters.kHNSCTL_dataStorageInstances[i].z])
            point.append(pointArray)

        # print(point)
        return point
    # Method to determine the distance to the cone
    def distanceToCone(self,point):
        # print('distanceToCone accessed')

        # print(point[0])
        # print(type(point[0]))
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

def main():
    # Loads test data with a known solution
    # ######
    # # Known solutons: -0.22888566,  0.24425689, -0.9640246
    # # The code works with this solution
    # #####
    # TLDataClass.TLData(0.13736903, -2.09331181,  1.176831, 5)
    # TLDataClass.TLData(0.19324891, -2.23147539,  1.20972186, 5)
    # TLDataClass.TLData(0.35961296, -3.67184001,  1.36968941, 5)
    # TLDataClass.TLData(0.38395479, -2.74271983,  1.23765356, 5)
    # TLDataClass.TLData(0.56420493, -3.09959046,  1.08545504, 5)
    # TLDataClass.TLData(-0.1346031 , -3.68954062,  1.19486776, 5)
    #
    # TLDataClass.TLData(0.33198168, -3.22328235,  0.31439186, 5)
    # TLDataClass.TLData(0.06276181, -3.60649323,  0.14596918, 5)
    # TLDataClass.TLData(0.85432262, -3.14077231,  0.15677479, 5)
    # TLDataClass.TLData(0.86477496, -3.5339717 ,  0.22202918, 5)
    # TLDataClass.TLData(2.94188149e-02,  -3.43052042e+00,  -3.14398441e-03, 5)
    # TLDataClass.TLData(0.50373139, -1.868233  ,  0.18008235, 5)

    optimizationTest = Optimization()
    optimizationTest.optimize()

if __name__ == '__main__':
    main()