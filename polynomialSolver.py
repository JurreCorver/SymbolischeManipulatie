from polynomials import *


#Check of input eq is really an equation. If it is move the right hand side to the left. If it is not try to interpret the result and give error.    
def eqtoexp(eq):    
    if type(eq) == EqNode:
        exp = simplify(eq.lhs - eq.rhs)
        return exp
    else:
        print("Input is not an equation. Try something in the form of 'a == b'.")
        print("Interpreting input as " + str(eq) + " == " + str(0) + ".")
        exp = eq
        return exp

#needs a variable and solution, the returns a list of expressions in the form xi = answer
def prepareSolutions(var, solutions):
    answers = []
    for i in range(0, len(solutions)):
            solutions[i] = simplify(solutions[i])
            answers.append(frost(var + str(i) + ' == ' + str(solutions[i])))
    return answers        

#Solves a linear polynomial requiring the variable and the coefficients    
def solveLinear(var, coef):
    sol =  Constant(0) - coef[0] / coef[1] 
    sol = simplify(sol)
    answer = frost(var + ' == ' + str(sol))
    return([answer])

#Solves a quadratic polynomial requiring the variable and the coefficients
def solveQuadratic(var, coef):
    deg = 2
    sol = [0 for i in range(0, deg)]
    #solutions using the quadratic formula
    Dscr =  (coef[1]) ** Constant(2) - Constant(4) * coef[2] * coef[0]
    
    #if int(Dscr.evaluate()) < 0:
    #    return []
    #else:     
    sol[0] = simplify((Constant(0) - coef[1] + (Dscr) ** Constant(0.5) ) / ( Constant(2) * coef[2] ))
    sol[1] = simplify((Constant(0) - coef[1] - (Dscr) ** Constant(0.5) ) / ( Constant(2) * coef[2] ))
    return(sol)
    
#Add extra functionality for special cases -> https://en.wikipedia.org/wiki/Cubic_function
def solveCubic(var, coef):
    deg = 3
    sol = [0 for i in range(0, deg)]
    u = [0 for i in range(0, 3)]
    u[0] = Constant(1)
    u[1] = frost('(-1 + i*(3**0.5)) / 2')
    u[2] = frost('(-1 - i*(3**0.5)) / 2')
    delta0 = coef[2] ** Constant(2) - Constant(3) * coef[3] * coef[1]
    delta1 = Constant(2) * (coef[2] ** Constant(3)) - Constant(9) * coef[3] * coef[2] * coef[1] + Constant(27) * coef[3] ** Constant(2) * coef[0]
    C = ( (delta1 + (delta1 ** Constant(2) - Constant(4)* delta0 ** Constant(3)  ) ** ( Constant(0.5) ) ) / Constant(2) )**(Constant(1) / Constant(3) )
    D = (Constant(-1) / (Constant(3) * coef[3] )) 
    
    for i in range(0, deg):
        sol[i] = simplify(D * (coef[2] + u[i] * C + delta0 / ( u[i] * C)))
    
    return sol    

#Solves Polynomials of degree 1 and 2
def solvePolynomial(eq, var):
    
    exp = eqtoexp(eq)
    solutions = []
    
    #Define the variable and check the degree of the equation and find the list of coefficients.
    #If the expression has negative powers of x, multiply to remove this negative factor
    var = str(var)
    mindeg = exp.mindeg(var)
    if mindeg <= -1:
        exp = simplify(exp * frost(var) ** Constant(-mindeg) )
    elif mindeg >= 1 and exp.deg(var) >= 4:
        exp = simplify(exp * frost(var) ** Constant(-mindeg) )
        solutions.append(Constant(0))
        
        
    
    deg = exp.deg(var)
    #Find the list of coefficients.
    #For a polynomial a x^3 + b x^2 + c, a = coef[3]
    coef = [0 for i in range(0, deg+1)]
    for i in range(0, deg+1):
        coef[i] = coefficient(exp, i, var)
    
    #checks if the expression is of the simple form x^k = constant, then solves it if this is true.
    checkstr = [int(str(coef[i])) for i in range(1, deg) ]
    if checkstr == [0 for i in range(1, deg) ]:
        ans = simplify(((Constant(0) - coef[0] ) / coef[-1] ) ** (Constant(1) / Constant(deg) ))
        solutions.append(ans)
        return prepareSolutions(var, solutions)

        
        
    #Return error when the degree is 0
    if deg == 0:
        #print("No solutions exist for an equation of degree " + str(deg) + ".")
        return []
    
    #Calculate solution for degree 1 polynomial    
    elif deg == 1:
        return solveLinear(var, coef)
    
    #Calculate solution for degree 2 polynomial    
    elif deg == 2:
        solutions += solveQuadratic(var, coef)
        return prepareSolutions(var, solutions)
    
    elif deg == 3:
        solutions += solveCubic(var, coef)
        return prepareSolutions(var, solutions)
    
        
    #Return error message for polynomials of degree greater than 2.
    else:
        print("Polynomial is of degree " + str(deg) + "." )
        print("This software doesn't solve polynomials of this degree.")
        return []