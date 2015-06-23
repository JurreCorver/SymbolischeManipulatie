from expression_template import *
import numpy as np

def numInt(expression, var, left, right, numsteps=10000):
    ans=0
    stepsize=abs(right-left)/numsteps
    points = np.arange(left, right, stepsize)
    l=len(points)
    for point in points:
        ans+= float(expression.evaluate({var.symbol:Constant(point)}))/l
    return Constant(ans)