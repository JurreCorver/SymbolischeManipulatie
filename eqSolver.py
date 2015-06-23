from expression_template import *


def findSide(exp, var, curdegree, degree):
    for i in range(curdegree, degree + 1):
        if exp.lhs.deg(var) == i and exp.rhs.deg(var) == i:
            return('lr')
        elif exp.lhs.deg(var) == i:
            return('l')
        elif exp.rhs.deg(var) == i:
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
    
def linSolve(exp, var):
        sol = Constant(0)
        location = exp
        while location != frost(var):
            if findSide(location, var, 1, 1) == 'l':
                #print('l')
                sol = solveStep(location, 'l', sol)    
                location = location.lhs
            elif findSide(location, var, 1,1) == 'r':
                #print('r')
                sol = solveStep(location, 'r', sol)
                location = location.rhs
        return sol 

#searches for the coefficient before a x^power, so for instance power = 2. a*x^2 + b x +c ==0 then it finds a        
def findcoefficient(exp, var, power):
    var = str(var)
    prevlocation = exp
    location = exp
    side = 'm'
    #print(type(location) != PowNode)
    #print(location.deg(var) != power)
    #print(exp.deg(var))
    #BUGSENSITIVE
    while (type(location) != PowNode or location.deg(var) > power ) and type(location) != Variable and type(location) != Constant:
        prevlocation = location
        if findSide(location, var, power, exp.deg(var)) == 'l':
            #print('l')
            side = 'l'
            location = location.lhs
                
        elif findSide(location, var, power, exp.deg(var)) == 'r':
            #print('r')
            side = 'r'
            location = location.rhs
    
    print(location)     
    if type(location) == Constant:
        return(location)
        print('test')
    
    
    if side == 'm':
        
        return(Constant(1))
        
        
    if side == 'l':         
        if type(prevlocation) == AddNode:
            return(Constant(1))
        elif type(prevlocation) == SubNode:
            return(Constant(1))
        elif type(prevlocation) == MulNode:
            return(prevlocation.rhs)
        elif type(prevlocation) == DivNode:
            return(Constant(1) / prevlocation.rhs)
        elif type(prevlocation) == PowNode:
            return(Constant(0))
        else:
            return(Constant(100000000))    
            
    if side == 'r':         
        if type(prevlocation) == AddNode:
            return(Constant(1))
        elif type(prevlocation) == SubNode:
            return(Constant(-1))
        elif type(prevlocation) == MulNode:
            return(prevlocation.lhs)
        elif type(prevlocation) == PowNode:
            return(Constant(0))
        #elif type(prevlocation) == DivNode:
        #    return(Constant(1) / prevlocation.rhs)
        else:
            return(Constant(100000000))         
            
            
'''def findConstant(exp, var):
    var = str(var)
    prevlocation = exp
    location = exp
    side = 'm'
    
    if type(exp) == Constant:
        return(exp)
    
    elif (type(exp) == AddNode or type(exp) == SubNode) '''  
    

def solvePolynomial(eq, var):
    exp = simplify(frost(str(eq)))
    var = str(var)
    sol = Constant(0)
    degree = exp.deg(str(var))
    '''Solves a polynomial like a x^2 + b x = c.  '''
    
    #Here we solve the linear equation
    if degree == 1:
        print('degree is 1')
        sol = simplify(linSolve(exp,var))
        return(sol)
        
    elif degree == 2:
        print('found degree 2 polynomial')
        a = findcoefficient(exp, var, 2)
        b = findcoefficient(exp, var, 1)
        print('finding constant')
        print(simplify(exp))
        c = findcoefficient(exp, var, 0)
        #c = Constant(0)
        print(c)
        sol1 = simplify(((b ** Constant(2) - Constant(4) * a * c) ** Constant(0.5) - b)/ (Constant(2) * a))
        sol2 = simplify((Constant(0) - (b ** Constant(2) - Constant(4) * a * c) ** Constant(0.5) - b)/ (Constant(2) * a))
        
        #TODO: check if both expressions are the same, if they are, only show one solution
        #TODO: Should return an expression once the equality operator is functional
        if sol1 == sol2:
            return(var + "=" + str(sol1))
        else:
            return('{' + var + '1 == ' + str(sol1) + ' and ' + var + '2 == ' + str(sol2) + '}')
        
        
    
  
    return('No solution found')   
    
                
   
        
    
        
    
    