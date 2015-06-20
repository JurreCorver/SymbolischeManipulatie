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


#print(d)
#print(c)

#print(Expression.fromString('5+2*3' )   )

#print(LogNode(a).evaluate())

#(simplify(frost('b*x + a*x**2+ b*x**2')))

#frost('a**x +b')

#print(frost('x+y'))

#solvePolynomial("x+y = 0")

#get commlist

#print(frost('x**2+2').deg())
#print('test')



print(solvePolynomial('3 + x-2', x))

#print(simplify(zero - solution))

#print(frost('2 == 2'))