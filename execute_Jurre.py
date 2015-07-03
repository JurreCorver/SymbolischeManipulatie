from expression_template import *
from functions import *




zero = Constant(0)
one = Constant(1)
a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
y = Variable('y')
expr = simplify(frost('x**3  == 1'))

l = solvePolynomial(expr, x)
[print(x) for x in l]


#x^2 +1/x

print(ExpNode( Constant((2j * math.pi) / 5 ) * Constant(2)  ) )


