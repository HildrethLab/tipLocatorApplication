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
import TLDataClass

# Optimization class
class Optimization():
    def __init__(self):
        print('Optimization class initiated')
        # Radius of the light entering the lens in mm
        self.radius = 0.5
        # Focal length of the lens in mm
        self.focalLength = 4

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
        for i in range(len(TLParameters.kHNSCTL_dataStorageInstances)):
            point[i]  = TLParameters.kHNSCTL_dataStorageInstances[i]

        print(point)
    # Method to determine the distance to the cone
    def distanceToCone(self,point):
        print('distanceToCone accessed')

        print(point[0])
        print(type(point[0]))
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
    ######
    # Known solutons: -0.22888566,  0.24425689, -0.9640246
    #####
    TLDataClass.TLData(0.13736903, -2.09331181,  1.176831, 5)
    TLDataClass.TLData(0.19324891, -2.23147539,  1.20972186, 5)
    TLDataClass.TLData(0.35961296, -3.67184001,  1.36968941, 5)
    TLDataClass.TLData(0.38395479, -2.74271983,  1.23765356, 5)
    TLDataClass.TLData(0.56420493, -3.09959046,  1.08545504, 5)
    TLDataClass.TLData(-0.1346031 , -3.68954062,  1.19486776, 5)

    point = []

    for i in range(len(TLParameters.kHNSCTL_dataStorageInstances)):
        point.append(TLParameters.kHNSCTL_dataStorageInstances[i])

    print(point)

    # optimizationTest = Optimization()
    # optimizationTest.optimize()

if __name__ == '__main__':
    main()