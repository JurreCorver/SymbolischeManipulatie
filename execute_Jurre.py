from expression_template import *
from functions import *
from eqSolver import *



zero = Constant(0)
a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
y = Variable('y')
d = a+b**c-x
solution = frost('a / b +c * d')
expres = frost('x**2  + x / 3 a + 3')


#print(expand(frost('(x+2)**2')))

#print('coefficient = ', findcoefficient(expres, 'x', 1) )

print(solvePolynomial('2 * x ** 2 + 8 * x', x))

#print(simplify(zero - solution))

#print(frost('2 == 2'))