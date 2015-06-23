from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')

print(leadingCoefficient(frost('5')))
print(polDivMod(frost('x+x**5+1+x**3'),frost('x**2')))