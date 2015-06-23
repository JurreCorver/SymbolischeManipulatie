from expression_template import *
from functions import *
from eqSolver import *



zero = Constant(0)
a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
y = Variable('y')
expr = frost('x**2 + 2*x')
#d = a + b ** c - x
#solution = frost('a / b + c * d')
#print(solution)
#expres = frost('x**2  + x / 3 a + 3')


#print(expand(frost('(x+2)**2')))

#print('coefficient = ', findcoefficient(expres, 'x', 1) )

print(solvePolynomial(expr, x))

#print(findSide(simplify(expr), 'x', 0, 2))
#print(expr.lhs)
#print(simplify(expr).lhs)
#print(simplify(frost('2 * (x + 2 * b +10 + 8 * x**2)')))

#print(simplify(zero - solution))

#print(frost('2 == 2'))

print(frost('x**2 + x +2'))