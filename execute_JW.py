from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')

print(frost('x**2-x**2').deg())
print(frost('-1*x**2+x**2').deg())
print(str(simplify(frost('x+5*x**2*(x+x**3)'))))
print(getCommList(simplify(frost('x+5*x**2*(x+x**3)')))[0])
print(leadingCoefficient(frost('x+x**5')))