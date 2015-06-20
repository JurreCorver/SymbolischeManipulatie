from expression_template import *


def findSide(expr, var, curdegree):
        if expr.lhs.deg(var) == curdegree and expr.rhs.deg(var) == curdegree:
            return('lr')
        elif expr.lhs.deg(var) == curdegree:
            return('l')
        elif expr.rhs.deg(var) == curdegree:
            return('r')
            
        print('error, could not find variable') 
        
def solveStep(exp, side, sol):
    if side == 'l':
        
        if type(exp) == AddNode:
            sol = sol - exp.rhs
        elif type(exp) == SubNode:
            sol = sol + exp.rhs
        elif type(exp) == MulNode:
            sol = sol / exp.rhs
        elif type(exp) == DivNode:
            sol = sol * exp.rhs
        else:
            return(-100000000)
    
    elif side == 'r':         
        if type(exp) == AddNode:
            sol = sol - exp.lhs 
        elif type(exp) == SubNode:
            sol = sol - exp.lhs  ##Because it is on the right side of the minus
        elif type(exp) == MulNode:
            sol = sol / exp.lhs #Needs fixing, cannot solve yet
        elif type(exp) == DivNode:
            sol = sol * exp.lhs
        else:
            return(-100000000)   
    
    return sol        
            
        
    



def solvePolynomial(eq, var):
    exp = simplify(frost(str(eq)))
    var = str(var)
    
    degree = exp.deg(str(var))
    '''Solves a polynomial like a x^2 + b x = c.  '''
    
    
    #print some information about the equation, for research purposes.
    '''print(exp)
    print(exp.lhs)
    print(exp.rhs)
    print(degree)'''
    
    #Here we solve the linear equation
    
    if degree == 1:
        sol = Constant(0)
        location = exp
        while location != frost(var):
            if findSide(location, var, 1) == 'l':
                #print('l')
                sol = solveStep(location, 'l', sol)    
                location = location.lhs
            elif findSide(location, var, 1) == 'r':
                #print('r')
                sol = solveStep(location, 'r', sol)
                location = location.rhs
    
    sol = simplify(sol)
    #print(0)
    #print(simplify(sol))
    return(sol)   
    
                
                
    
    print(type(exp) == AddNode)            
                
            
    
    
            
    
    return(0)
        
    
        
    
    