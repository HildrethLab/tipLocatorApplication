'''
Circle fitting module for the tip locator application.
Accepts the input of data points and fits a 2D circle to the data points
'''

## Imports
# Built in imports
import numpy as np
from math import sqrt
# Custom imports

class CircleFit():
    def __init__(self):
        print('FitCircle __init__ accessed')

    # Method for fitting the circle, pass in orthoginal coordinate point data to fit
    def fitCircle(self,x,y):

        x = np.squeeze(np.asarray(x))
        y = np.squeeze(np.asarray(y))

        # print('fitCircle accessed')
        coefA = np.matrix((x, y, np.ones(len(x)))).getT()
        coefB = []

        for i in  range(0,len(x)):
            coefB.append(-(x[i]**2+y[i]**2))

        coefB = np.matrix(coefB).getT()

        # print(coefA)
        # print(coefB)

        coefficients = np.linalg.lstsq(coefA,coefB)

        print(coefficients[0])

        center_X = -0.5 * coefficients[0][0]
        center_Y = -0.5 * coefficients[0][1]

        radius = sqrt((coefficients[0][0]**2 + coefficients[0][1]**2)/4 - coefficients[0][2])
        # print(center_X,center_Y,radius)

        return(center_X,center_Y,radius,coefficients)