from expression_template import *
import numpy as np

def numInt(expression, var, left, right, numsteps=10000):
    ans=0

    #convert the constants in the input to numbers
    left=float(left)
    right=float(right)
    numsteps=float(numsteps)
    stepsize=abs(right-left)/(numsteps-1) #-1 because right should always be the last point

    #create a set of points where we evaluate the expression
    points =  np.append(np.arange(left, right, stepsize),right)
    l=len(points)
    for point in points:
        ans+= num(expression.evaluate({var.symbol:Constant(point)}))/l #neem het gemiddelde over alle punten waar de
    return Constant(ans)

methodList.append(['numIntegrate',numInt,5])