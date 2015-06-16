from expression_template import *
import numpy as np

def numInt(exp, var, left, right, stepsize=0.1):
    ans=0
    points = np.arange(left, right, stepsize)
    l=len(points)
    for point in points:
        ans+= float(exp.evaluate({var.symbol:point}))/l
    return ans

x=Variable('x')
print(numInt(frost('sin(x)'),x,1,2))