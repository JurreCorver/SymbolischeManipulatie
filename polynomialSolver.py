from polynomials import *


#Solves Polynomials of degree 1 and 2
def solvePolynomial(eq, var):
    #Check of input eq is really an equation. If it is move the right hand side to the left. If it is not try to interpret the result and give error.
    if type(eq) == EqNode:
        exp = simplify(eq.lhs - eq.rhs)
    else:
        print("Input is not an equation. Try something in the form of 'a == b'.")
        print("Interpreting input as " + str(eq) + " == " + str(0) + ".")
        exp = eq
    
    #Define the variable, the degree of the equation and find the list of coefficients. 
    #For a polynomial a x^3 + b x^2 + c, a = coef[3] 
    var = str(var)
    deg = exp.deg(var)
    coef = [0 for i in range(0, deg+1)]
    for i in range(0, deg+1):
        coef[i] = coefficient(exp, i, var)
    
    #Return error when the degree is 0
    if deg == 0:
        print("No solutions exist for an equation of degree " + str(deg) + ".")
        return('error')
    
    #Calculate solution for degree 1 polynomial    
    elif deg == 1:
        sol =  Constant(0) - coef[0] / coef[1] 
        sol = simplify(sol)
        answer = frost(var + ' == ' + str(sol))
        return(answer)
    
    #Calculate solution for degree 2 polynomial    
    elif deg == 2:
        sol = [0 for i in range(0, deg)]
        answer = [0 for i in range(0, deg)]
        #solutions using the quadratic formula
        sol[0] = (Constant(0) - coef[1] + (coef[1] ** Constant(2) - Constant(4) * coef[2] * coef[0] ) ** Constant(0.5) ) / ( Constant(2) * coef[2] )
        sol[1] = (Constant(0) - coef[1] - (coef[1] ** Constant(2) - Constant(4) * coef[2] * coef[0] ) ** Constant(0.5) ) / ( Constant(2) * coef[2] )
        
        for i in range(0, deg):
            sol[i] = simplify(sol[i])
            answer[i] = frost(var + str(i) + ' == ' + str(sol[i]))
            
        return(answer)
        
    #Return error message for polynomials of degree greater than 2.
    else:
        print("Polynomial is of degree " + str(deg) + "." )
        print("This software doesn't solve polynomials of this degree.")
        return('error')
        