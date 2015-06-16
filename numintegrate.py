from expression_template import *
import numpy as np

def numInt(exp, var, left, right, numsteps=10000):
    ans=0
    stepsize=abs(right-left)/numsteps
    points = np.arange(left, right, stepsize)
    l=len(points)
    for point in points:
        ans+= float(exp.evaluate({var.symbol:point}))/l
    return ans