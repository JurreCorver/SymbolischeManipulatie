from polynomials import *

def solvePolynomial(eq, var):
    exp = simplify(eq)
    var = str(var)
    deg = eq.deg(var)
    coef = [0 for i in range(0, deg+1)]
    
    for i in range(0, deg+1):
        coef[i] = coefficient(exp, i, var)
        
    if deg == 1:
        sol =  Constant(0) - coef[0] / coef[1] 
        sol = simplify(sol)
        answer = frost(var + ' == ' + str(sol))
        return(answer)
    elif deg == 2:
        sol = [0 for i in range(0, deg)]
        answer = [0 for i in range(0, deg)]
        #solutions using the quadratic formula
        sol[0] = (Constant(0) - coef[1] + (coef[1] ** Constant(2) - Constant(4) * coef[2] * coef[0] ) ** Constant(0.5) ) / ( Constant(2) * coef[2] )
        sol[1] = (Constant(0) - coef[1] - (coef[1] ** Constant(2) - Constant(4) * coef[2] * coef[0] ) ** Constant(0.5) ) / ( Constant(2) * coef[2] )
        
        for i in range(0, deg):
            sol[i] = simplify(sol[i])
            answer[i] = frost(var + str(i) + ' == ' + str(sol[i]))
            
        
        
        
        
    
    
    