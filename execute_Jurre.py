from expression_template import *
from functions import *
from eqSolver import *



a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
d = a+b**c-x


#print(d)
#print(c)

#print(Expression.fromString('5+2*3' )   )

#print(LogNode(a).evaluate())

#(simplify(frost('b*x + a*x**2+ b*x**2')))

#frost('a**x +b')

#print(frost('x+y'))

#solvePolynomial("x+y = 0")

#get commlist

print(frost('x**2+2').deg())
#print('test')