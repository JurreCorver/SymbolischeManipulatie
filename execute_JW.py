from expression_template import *

a = Constant(2)
b = Constant(3)
c = Constant(4)
x = Variable('x')
exp1=frost('2*(x-5)*3')
exp2=frost('2*(x-5)')
exp3=sfrost('1')
var='x'

print(polGcd(exp1,exp2))
