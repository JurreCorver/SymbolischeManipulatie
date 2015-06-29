from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
exp1=frost('5*(x-1)*(x-3/5)')
exp2=frost('2*(x-1)')
exp3=sfrost('1')
var=frost('x')

print(simplify(exp1))
print(simplify(exp2))
print(polRem(exp2,exp1,var))
print(polGcd(exp1,exp2,var))
#print(simplify(exp1))
#print(exp1.deg(frost('x')))
#print(exp1.mindeg(frost('x')))